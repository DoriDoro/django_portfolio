from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class JournalPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Journal.Status.PUBLISHED)


class Journal(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        "journal.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="journal_category",
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    content = HTMLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="journal_user",
    )
    links = models.ManyToManyField("journal.Link", blank=True, related_name="links")

    objects = models.Manager()
    journal_published = JournalPublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("journal:journal-detail", args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    published = models.BooleanField(
        default=True, verbose_name=_("journal category visible on website")
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=200)
    platform = models.ForeignKey(
        "journal.Platform", on_delete=models.CASCADE, related_name="link_platform"
    )
    url = models.URLField()
    published = models.BooleanField(
        default=True, verbose_name=_("journal link visible on website")
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Platform(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
