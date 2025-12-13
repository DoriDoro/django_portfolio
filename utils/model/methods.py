from django.core.exceptions import ValidationError


def validate_not_blank(value: str):
    if not value or not value.strip():
        raise ValidationError("Question cannot be empty or whitespace.")
