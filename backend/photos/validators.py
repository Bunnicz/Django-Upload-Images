from os.path import splitext
from typing import Optional

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import ImageField
from rest_framework.request import Request

image_max_size: int = settings.UPLOAD_FILE_MAX_SIZE_MB
allowed_image_types: dict = settings.WHITELISTED_IMAGE_TYPES
url_expiration_time_range: list = settings.URL_EXPIRATION_TIME_RANGE


def validate_image(image: ImageField):
    """Validate image: existence, disk size, extension, content-type"""
    if image is None:
        raise ValidationError("No image was provided!")
    if image.size > image_max_size * 1024 * 1024:
        raise ValidationError(f"Image max size is {image_max_size} MB!")
    extension = splitext(image.name)[1]
    if extension not in allowed_image_types.keys():
        raise ValidationError(f"Image format {extension} is not supported!")
    if image.content_type not in allowed_image_types.values():
        raise ValidationError(f"Invalid image content-type: {image.content_type}!")


def validate_url_expiration_time(user: Request.user, delete_url_time: Optional[int]):
    """Validate url expiration time and"""
    if not user.tier.generated_url and delete_url_time:
        raise ValidationError(
            f"User with a tier {user.tier} can't fetch an expiring link. Get a higher tier!"
        )
    if delete_url_time is not None:
        if user.tier.generated_url and (
            delete_url_time < url_expiration_time_range[0]
            or delete_url_time > url_expiration_time_range[1]
        ):
            raise ValidationError(
                f"Image expiration time must be between {url_expiration_time_range[0]} and {url_expiration_time_range[1]} seconds!"
            )
