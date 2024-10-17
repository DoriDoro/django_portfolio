from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    content = models.TextField()
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

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["publish"]),
        ]

    def __str__(self):
        return self.title
