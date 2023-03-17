import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Image(models.Model):
    """Image model"""

    class Meta:
        db_table = "images"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.image.url

    def generate_filename(instance, filename: str) -> str:
        f_hash = str(uuid.uuid4()).replace("-", "")
        assert len(f_hash) % 2 == 0
        return "{}{}{}".format(
            os.sep.join(x + y for x, y in zip(f_hash[::2], f_hash[1::2])), os.sep, filename
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=generate_filename)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images"
    )
    img_px200 = ImageSpecField(
        source="image",
        processors=[ResizeToFill(150, 200)],
        format="png",
        options={"quality": 75},
    )
    img_px400 = ImageSpecField(
        source="image",
        processors=[ResizeToFill(300, 400)],
        format="png",
        options={"quality": 75},
    )
    delete_url_time = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class TempUrl(models.Model):
    """Temporary Url model for expiring link to the Image"""

    class Meta:
        db_table = "temp_urls"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.token

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=32,
        default=get_random_string(length=32),
        blank=False,
        null=False,
        unique=True,
    )
    expiration_date = models.DateTimeField(null=False, blank=False)
