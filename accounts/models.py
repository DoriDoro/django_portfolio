from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

from utils.database.validators import validate_not_blank


class User(AbstractUser):
    """Inherit AbstractUser from Django."""

    pass


class Profile(models.Model):

    phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)

    introduction = HTMLField(validators=[validate_not_blank])
    dream_job = HTMLField(validators=[validate_not_blank])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        return self.user.username
