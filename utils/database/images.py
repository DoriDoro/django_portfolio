import logging
import os
import uuid

from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model
from PIL import Image, UnidentifiedImageError


# -- Logger --
logger = logging.getLogger(__name__)


def upload_to(instance: Model, filename: str):
    """Return a unique upload path in the form uploads/<model>/<uuid>.<ext>."""

    ext = os.path.splitext(filename)[1].lower()
    model_name = instance.__class__.__name__.lower()
    random_filename = uuid.uuid4().hex
    return f"uploads/{model_name}/{random_filename}{ext}"


def private_storage():
    """Return the private storage backend; raises KeyError if it is not configured in STORAGES."""

    try:
        return storages["private"]
    except KeyError as exc:
        logger.error(f"Private storage backend not available: {exc}")
        raise KeyError(
            "Private storage backend not configured in settings.py."
            "Ensure 'private' is defined in settings.STORAGES."
        ) from exc


def _safe_seek(file_obj, offset: int = 0) -> None:
    """Seek the file stream to offset, silently ignoring streams that do not support seeking."""

    try:
        file_obj.seek(offset)
    except (OSError, ValueError):
        logger.debug("Unable to seek uploaded file stream.", exc_info=True)


def validate_image_file(uploaded_file: UploadedFile | None) -> UploadedFile | None:
    """Validate that the file is a JPEG/PNG/GIF/WEBP image under 5 MB with a passing integrity check."""

    if uploaded_file is None:
        return uploaded_file

    max_bytes = 5 * 1024 * 1024  # 5 MB
    if getattr(uploaded_file, "size", 0) > max_bytes:
        raise ValidationError(f"Image file is too large (max {max_bytes}MB).")

    allowed_formats = {"JPEG", "PNG", "GIF", "WEBP"}

    # Ensure we're at the beginning of the stream
    uploaded_file.seek(0)

    try:
        # 1) Verify the file is an image (quick integrity check)
        img = Image.open(uploaded_file)
        img.verify()  # quick integrity check; file becomes unusable afterward

        # 2) Re-open for metadata access
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)

        if not img.format or img.format.upper() not in allowed_formats:
            raise ValidationError(
                f"Unsupported image format. Allowed: {', '.join(sorted(allowed_formats))}."
            )

    except UnidentifiedImageError:
        raise ValidationError("Uploaded file is not a valid image.")
    except (OSError, ValueError):
        # OSError often catches truncated/corrupted images
        raise ValidationError("Image file is corrupted or unreadable.")
    finally:
        _safe_seek(uploaded_file)

    return uploaded_file
