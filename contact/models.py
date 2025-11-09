from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

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
        indexes = [
            models.Index(fields=["email", "submitted_at"], name="ix_email_submitted")
        ]
        ordering = ["-submitted_at"]
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    def __str__(self):
        return f"Message from {self.first_name} - {self.email}"


class Category(SlugCreateMixin, models.Model):
    """
    To categorize incoming contact requests in Admin.
    SlugCreateMixin: auto-generate 'slug' from 'name'.
    """

    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, editable=False)

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
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uix_contact_cat_low_name")
        ]
        indexes = [
            models.Index(fields=["name", "active"], name="idx_contact_name_active")
        ]
        ordering = [Lower("name"), "pk"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Category.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"name": f"Category with name: '{self.name}' exists already."}
            )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        # make sure clean() gets called
        self.full_clean()
        self.create_unique_slug(Category)

        super().save(*args, **kwargs)
