from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class ContactRequest(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=200)
    message = HTMLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_category",
    )

    class Meta:
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"

    def __str__(self):
        return f"Message from {self.first_name} - {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    published = models.BooleanField(
        default=True, verbose_name=_("contact category visible on website")
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
