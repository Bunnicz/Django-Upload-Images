from django.contrib import admin
from django.utils import timezone  # time-zone aware datetime
from imagekit import ImageSpec
from imagekit.admin import AdminThumbnail
from imagekit.cachefiles import ImageCacheFile
from imagekit.processors import ResizeToFill

from .models import Image, TempUrl


class AdminThumbnailSpec(ImageSpec):
    """Admin panel Image thumbnail custom processor"""

    processors = [ResizeToFill(100, 30)]
    format = "JPEG"
    options = {"quality": 60}


def cached_admin_thumb(instance: Image) -> Image:
    """Returns cached thumbnail of the image for the admin panel"""

    cached = ImageCacheFile(AdminThumbnailSpec(instance.image))
    cached.generate()
    return cached


class ImageAdmin(admin.ModelAdmin):
    """Admin panel Image model config"""

    list_display = (
        "id",
        "__str__",
        "admin_thumbnail",
        "user",
        "delete_url_time",
        "timestamp",
    )
    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)


class TempUrlAdmin(admin.ModelAdmin):
    list_display = ("id", "token", "expiration_date", "get_is_expired")
    readonly_fields = [
        "get_is_expired",
    ]

    @admin.display(
        boolean=True,
        description="Has Expired?",
    )
    def get_is_expired(self, instance: TempUrl) -> bool:
        """Returns tick or cross on the Admin Panel"""
        is_expired = True if timezone.now() > instance.expiration_date else False
        return is_expired


admin.site.register(Image, ImageAdmin)
admin.site.register(TempUrl, TempUrlAdmin)
