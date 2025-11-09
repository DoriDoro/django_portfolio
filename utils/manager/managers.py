from django.db import models


class ActiveManager(models.Manager):
    """Custom manager to filter the queryset for 'active=True'."""

    def get_queryset(self):
        return super().get_queryset().filter(active=True)
