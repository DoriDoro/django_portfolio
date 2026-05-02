from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

from utils.database.validators import validate_not_blank


class User(AbstractUser):
    """Custom user model; currently a direct passthrough for AbstractUser."""

    pass


class Profile(models.Model):
    """Personal profile data linked one-to-one with the site owner's User account."""

    phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)
    motto = models.CharField(max_length=150)

    introduction = HTMLField(validators=[validate_not_blank])
    more_details = HTMLField(validators=[validate_not_blank])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        return self.user.username

    def _normalize_fields(self):
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        if self.address:
            self.address = self.address.strip()
        if self.profession:
            self.profession = self.profession.strip()
        if self.motto:
            self.motto = self.motto.strip()
        if self.introduction:
            self.introduction = self.introduction.strip()
        if self.more_details:
            self.more_details = self.more_details.strip()

    def save(self, *args, **kwargs):
        """Pass clean=False to skip full_clean(), e.g. in management commands."""
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)
