from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from utils.database.managers import ActiveManager
from utils.database.validators import validate_not_blank
from utils.database.slug import SlugCreateMixin


class ContactRequest(models.Model):
    """
    For any contact requests on the website.
    HTMLField(): enables specific non-HTML elements.
    """

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField(max_length=250)

    subject = models.CharField(max_length=200)
    message = HTMLField(validators=[validate_not_blank])

    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(first_name="") & ~Q(email="") & ~Q(subject=""),
                name="ck_contact_first_email",
                violation_error_code="check",
                violation_error_message=_(
                    "Your first name, the email address and the subject are required."
                ),
            ),
        ]
        indexes = [
            models.Index(
                fields=["category", "-submitted_at"],
                name="idx_contact_category_submitted",
            ),
            models.Index(
                Lower("email"),
                Lower("first_name"),
                name="idx_contact_first_name_email",
            ),
        ]
        ordering = ["-submitted_at"]
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    def __str__(self):
        return f"Message from {self.first_name} - {self.email}"

    def _normalize_fields(self):
        if self.first_name:
            self.first_name = self.first_name.strip()

        if self.last_name:
            self.last_name = self.last_name.strip()

        if self.email:
            self.email = self.email.strip().lower()

        if self.subject:
            self.subject = self.subject.strip()

    def clean(self):
        super().clean()
        errors: dict[str, str] = {}

        # Normalize fields
        self._normalize_fields()

        cutoff = timezone.now() - timedelta(days=14)
        qs = ContactRequest.objects.filter(
            first_name__iexact=self.first_name,
            email__iexact=self.email,
            subject__iexact=self.subject,
            submitted_at__gte=cutoff,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                _(
                    "This request was already submitted recently. "
                    "Please wait 14 days before resubmitting."
                )
            )

        # Prevent assigning an inactive category
        # internal usage
        if self.category and not self.category.active:
            errors["category"] = "Selected category is inactive."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self._normalize_fields()
        self.full_clean()
        return super().save(*args, **kwargs)


class Category(SlugCreateMixin, models.Model):
    """
    To categorize incoming contact requests in Admin.
    SlugCreateMixin: auto-generate 'slug' from 'name'.
    """

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True, editable=False)

    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # --- Managers ---
    objects = models.Manager()
    active_categories = ActiveManager()

    class Meta:
        # Case-insensitive uniqueness on name at DB level
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uq_contact_cat_lower_name",
                violation_error_code="unique",
                violation_error_message=_("The category name already exists."),
            ),
        ]
        indexes = [
            # For lookups and ordering using Lower("name")
            models.Index(
                Lower("name"),
                "active",
                name="idx_contact_cat_name_active",
            ),
        ]
        ordering = [Lower("name"), "pk"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        self._normalize_fields()

        if self.pk:
            old_name = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("name", flat=True)
                .first()
            )
            if old_name != self.name:
                self.slug = ""

        if not self.slug and self.name:
            self.create_unique_slug(Category)

        self.full_clean()
        super().save(*args, **kwargs)
