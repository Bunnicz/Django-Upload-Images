from django.utils import timezone  # time-zone aware datetime
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Image, TempUrl
from .validators import validate_image, validate_url_expiration_time


class ImageSerializer(serializers.ModelSerializer):
    """Image serializer class"""

    img_px200 = serializers.SerializerMethodField(read_only=True)
    img_px400 = serializers.SerializerMethodField(read_only=True)
    img_native = serializers.SerializerMethodField(read_only=True)
    temp_url = serializers.SerializerMethodField(read_only=True)
    delete_url_time_left_second = serializers.SerializerMethodField(read_only=True)
    delete_url_time = serializers.IntegerField(required=False, default=None)

    class Meta:
        model = Image
        fields = [
            "id",
            "image",
            "img_px200",
            "img_px400",
            "img_native",
            "temp_url",
            "delete_url_time",
            "delete_url_time_left_second",
        ]
        write_only_field = ["image", "delete_url_time"]

    def validate(self, data, *args, **kwargs) -> dict:
        """Validate Data"""
        request = self.context.get("request")
        print(request)
        print(request.data)
        print(data)

        data["user"] = request.user
        image = data.get("image")
        delete_url_time = data.get("delete_url_time")  # ,0)
        validate_image(image)
        validate_url_expiration_time(request.user, delete_url_time)
        return data

    def create(self, validated_data: dict, *args, **kwargs) -> Image:
        """Override create function. Returns Image object.
        Creates TempUrl while Image is being created with expiring link time."""
        image_created = super().create(validated_data, *args, **kwargs)
        if (
            image_created
            and image_created.user.tier.generated_url
            and image_created.delete_url_time is not None
        ):
            expiration_date = timezone.now() + timezone.timedelta(
                seconds=int(image_created.delete_url_time)
            )
            temp_url = TempUrl(image=image_created, expiration_date=expiration_date)
            temp_url.save()
        return image_created

    def to_representation(self, instance: Image, *args, **kwargs) -> dict:
        """Returns ONLY the fields avaible for current user tier - DRF Response"""
        data_to_return = super(ImageSerializer, self).to_representation(instance)
        data_to_return.pop("id")
        data_to_return.pop("image")
        data_to_return.pop("delete_url_time")
        if not instance.user.tier.img_native:
            data_to_return.pop("img_native")
        if not instance.user.tier.img_px400:
            data_to_return.pop("img_px400")
        if not instance.user.tier.generated_url or instance.delete_url_time is None:
            data_to_return.pop("delete_url_time_left_second")
            data_to_return.pop("temp_url")
        else:
            now_time = timezone.now()
            delete_time = instance.timestamp + timezone.timedelta(
                seconds=int(instance.delete_url_time)
            )
            if now_time > delete_time:
                data_to_return.pop("delete_url_time_left_second")
                data_to_return.pop("temp_url")

        return data_to_return

    def get_img_px200(self, instance: Image, *args, **kwargs) -> str:
        """Returns url for 200px thumbnail image"""
        request = self.context.get("request")
        if instance.user.tier.img_px200:
            return request.build_absolute_uri(instance.img_px200.url)

    def get_img_px400(self, instance: Image, *args, **kwargs) -> str:
        """Returns url for 400px thumbnail image"""
        request = self.context.get("request")
        if instance.user.tier.img_px400:
            return request.build_absolute_uri(instance.img_px400.url)

    def get_img_native(self, instance: Image, *args, **kwargs) -> str:
        """Returns url for original size image"""
        request = self.context.get("request")
        if instance.user.tier.img_native:
            return request.build_absolute_uri(instance.image.url)

    def get_temp_url(self, instance: Image, *args, **kwargs) -> str:
        """Returns absolute expiring url"""
        if instance.user.tier.generated_url and instance.delete_url_time is not None:
            request = self.context.get("request")
            temp_url = TempUrl.objects.select_related("image").get(image=instance.id)
            return reverse("temp-url", request=request, args=[temp_url.token])

    def get_delete_url_time_left_second(self, instance: Image, *args, **kwargs) -> int:
        """Returns amount of seconds left to delete url to image"""
        if instance.delete_url_time is None:
            return 0
        delete_time = instance.timestamp + timezone.timedelta(
            seconds=int(instance.delete_url_time)
        )
        time_left = delete_time - timezone.now()
        return time_left.seconds
