from django.core.exceptions import ValidationError


def validate_not_blank(value: str):
    """Raise ValidationError if the value is None, empty, or contains only whitespace."""
    if not value or not value.strip():
        raise ValidationError("This field cannot be empty or whitespace.")
