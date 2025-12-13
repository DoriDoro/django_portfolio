from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from typing import Dict

from utils.manager.managers import ActiveManager
from utils.slug.mixins import SlugCreateMixin


class ContactRequest(models.Model):
    """
    For any contact requests on the website.
    HTMLField(): enables specific non-HTML elements.
    """

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=250)

    subject = models.CharField(max_length=200)
    message = HTMLField()

    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_category",
    )

    class Meta:
        constraints = [
            # Ensure basic non-empty data at DB level (prevents all-spaces values)
            models.CheckConstraint(
                check=~Q(first_name__exact="") & ~Q(email__exact=""),
                name="ck_contact_not_empty_firstname_email",
            )
        ]
        indexes = [
            # Common pattern: filter by category, order by submitted_at
            models.Index(
                fields=["category", "-submitted_at"],
                name="idx_contact_category_submitted",
            ),
            # If you frequently filter by lowercase email, this helps
            models.Index(
                Lower("email"),
                name="idx_contact_lower_email",
            ),
        ]
        ordering = ["-submitted_at"]
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    def __str__(self):
        return f"Message from {self.first_name} - {self.email}"

    def clean(self):
        errors: Dict[str, str] = {}

        # Normalize fields
        if self.first_name:
            self.first_name = self.first_name.strip()

        if self.last_name:
            self.last_name = self.last_name.strip()

        if self.email:
            self.email = self.email.strip().lower()

        if self.subject:
            self.subject = self.subject.strip()

        # First name must not be only whitespace
        if not self.first_name:
            errors["first_name"] = "First name cannot be blank."

        # Email must not be blank (DB CheckConstraint also enforces this)
        if not self.email:
            errors["email"] = "Email cannot be blank."

        # Prevent assigning an inactive category
        if self.category and not self.category.active:
            errors["category"] = "Selected category is inactive."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Category(SlugCreateMixin, models.Model):
    """
    To categorize incoming contact requests in Admin.
    SlugCreateMixin: auto-generate 'slug' from 'name'.
    """

    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True, editable=False)

    active = models.BooleanField(
        default=True,
        verbose_name=_("contact category visible on website"),
        db_index=True,
    )

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
                name="uix_contact_cat_lower_name",
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
        ordering = ["name", "pk"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def clean(self):
        errors: Dict[str, str] = {}

        if not self.name:
            errors["name"] = "Name cannot be blank."

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Category.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Category with name: '{self.name}' exists already."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        if not self.slug and self.name:
            self.create_unique_slug(Category)

        self.full_clean()
        super().save(*args, **kwargs)
