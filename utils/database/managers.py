from django.db import models


class ActiveManager(models.Manager):
    """Custom manager that filters the default queryset to active=True records only."""

    def get_queryset(self):
        return super().get_queryset().filter(active=True)
