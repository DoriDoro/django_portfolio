import logging

from django.core.exceptions import FieldError
from django.db import DatabaseError
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class SlugCreateMixin:
    """Generates slug from specific field_name automatically."""

    def create_unique_slug(self, model_class, field_name="name", slug_field="slug"):
        try:
            name = getattr(self, field_name)
            if not name:
                raise ValueError(f"'{field_name}' is missing or empty.")

            if not getattr(self, slug_field):
                base_slug = slugify(name)
                slug = base_slug

                counter = 1
                while model_class.objects.filter(**{slug_field: slug}).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                setattr(self, slug_field, slug)

        except AttributeError as e:
            logger.exception(f"Missing field: '{e}'.")
            raise AttributeError(
                f"Model is missing required field: '{field_name}' or '{slug_field}'."
            ) from e
        except FieldError as e:
            logger.exception(f"Invalid filed used in query: '{e}'.")
            raise ValueError(
                f"Invalid slug field: '{slug_field}' in model query."
            ) from e
        except DatabaseError as e:
            logger.exception(f"Database error during slug generation: '{e}'.")
            raise RuntimeError(
                "Database error while checking for existing slugs."
            ) from e
        except Exception as e:
            logger.exception(
                f"Unexpected error occurred during slug generation: '{e}'."
            )
            raise RuntimeError("Unexpected error occurred during slug creation.") from e
