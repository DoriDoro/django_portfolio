from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from typing import Dict

from utils.manager.managers import ActiveManager
from utils.slug.mixins import SlugCreateMixin


class JournalPublishedManager(models.Manager):
    """Filters queryset by 'status=PUBLISHED'."""

    def get_queryset(self):
        return super().get_queryset().filter(status=Journal.Status.PUBLISHED)


class Journal(SlugCreateMixin, models.Model):
    """The steps of my projects."""

    class Status(models.TextChoices):
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    content = HTMLField()

    publish = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_journals",
    )
    category = models.ForeignKey(
        "journal.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_journals",
    )
    links = models.ManyToManyField(
        "journal.Link", blank=True, related_name="link_journals"
    )

    objects = models.Manager()
    published_journals = JournalPublishedManager()

    class Meta:
        ordering = ["-publish", "-created"]
        indexes = [
            models.Index(fields=["status", "-publish"], name="idx_journal_status_pub"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("journal:journal-detail", kwargs={"slug": self.slug})

    def clean(self):
        errors: Dict[str, str] = {}

        # Status / publish logic
        if self.status == Journal.Status.PUBLISHED:
            # Avoid publishing with a future date
            if self.publish and self.publish > timezone.now():
                errors["publish"] = (
                    "A published journal cannot have a publish date in the future."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.strip()

        if not self.slug and self.title:
            self.create_unique_slug(Journal, field_name="title")

        self.full_clean()
        super().save(*args, **kwargs)


class Category(SlugCreateMixin, models.Model):
    """Category of a Journal."""

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True, editable=True)

    active = models.BooleanField(
        default=True,
        verbose_name=_("journal category visible on website"),
        db_index=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_categories = ActiveManager()

    class Meta:
        constraints = [models.UniqueConstraint(Lower("name"), name="uix_cat_low_name")]
        indexes = [models.Index(fields=["name", "active"], name="idx_cat_name_active")]
        ordering = ["name", "pk"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Category.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"A Category with name: {self.name} exists already."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        if not self.slug and self.name:
            self.create_unique_slug(Category)

        self.full_clean()
        super().save(*args, **kwargs)


class Link(models.Model):
    """Link to a Website/Platform."""

    title = models.CharField(max_length=200)
    url = models.URLField()

    active = models.BooleanField(
        default=True, verbose_name=_("journal link visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    platform = models.ForeignKey(
        "journal.Platform", on_delete=models.CASCADE, related_name="links"
    )

    objects = models.Manager()
    active_links = ActiveManager()

    class Meta:
        constraints = [
            # Same URL should not be duplicated per platform
            models.UniqueConstraint(
                fields=["platform", "url"],
                name="link_platform_url_unique",
            ),
            # Title should be unique per Platform
            models.UniqueConstraint(
                Lower("title"), "platform", name="uix_link_low_title_platform"
            ),
        ]
        indexes = [
            models.Index(fields=["title", "active"], name="idx_link_title_active")
        ]
        ordering = ["title", "pk"]

    def __str__(self):
        return self.title

    def clean(self):
        errors: Dict[str, str] = {}

        if self.title:
            self.title = self.title.strip()

        # Enforce Title/Platform uniqueness
        if self.title and self.platform.id:
            if (
                Link.objects.filter(title__iexact=self.title, platform=self.platform)
                .exclude(pk=self.pk)
                .exists()
            ):
                errors["title"] = f"Link with name: '{self.title}' exists already."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Platform(SlugCreateMixin, models.Model):
    """Details of the Platform."""

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uix_platform_low_name")
        ]
        ordering = ["name", "pk"]

    def __str__(self):
        return self.name

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Platform.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Platform with name: '{self.name}' exists already."

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        if not self.slug and self.name:
            self.create_unique_slug(Platform)

        self.full_clean()
        super().save(*args, **kwargs)
