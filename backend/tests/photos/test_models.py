from factory.django import ImageField
from pytest import mark

from photos.models import Image, TempUrl


class TestImageModel:
    """Image model test cases"""

    def test_build_image_without_delete_url_time(self, image_factory: Image):
        image = image_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            image=ImageField(filename="test_image", format="JPEG"),
        )
        assert image.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert image.user
        assert not image.delete_url_time

    def test_str_method(self, image_factory: Image):
        image = image_factory.build(
            image=ImageField(filename="test_image", format="JPEG"),
        )
        assert str(image) == "/media/test_image"

    @mark.django_db
    def test_create_image_with_delete_url_time(self, image_factory: Image):
        image = image_factory.create(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            image=ImageField(filename="test_image", format="JPEG"),
            with_delete_url_time=True,
        )
        count = TempUrl.objects.all().count()
        assert image.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert image.delete_url_time
        assert count == 1

    @mark.django_db
    def test_create_batch_images(self, image_factory: Image):
        image_factory.create_batch(20)
        count = Image.objects.all().count()
        assert count == 20

    @mark.django_db
    def test_create_batch_images_with_delete_url_time(self, image_factory: Image):
        image_factory.create_batch(20, with_delete_url_time=True)
        count = TempUrl.objects.all().count()
        assert count == 20


class TestTempUrlModel:
    """TempUrl model test cases"""

    def test_build_temp_url(self, temp_url_factory: TempUrl, test_image_jpeg: Image):
        temp_url = temp_url_factory.build(
            id="fba78912-0b65-4fd8-9e19-8b89035f34c0",
            image=test_image_jpeg,
            token="wprjISNzhzsBHwSVKjMbvHEOqOchMhJX",
            expiration_date="2023-03-17 16:46:36.906634+00:00",
        )
        assert temp_url.id == "fba78912-0b65-4fd8-9e19-8b89035f34c0"
        assert str(temp_url.image) == "/media/test_image"
        assert temp_url.token == "wprjISNzhzsBHwSVKjMbvHEOqOchMhJX"
        assert temp_url.expiration_date == "2023-03-17 16:46:36.906634+00:00"

    def test_str_method(self, temp_url_factory: TempUrl):
        temp_url = temp_url_factory.build(
            token="wprjISNzhzsBHwSVKjMbvHEOqOchMhJX",
        )
        assert str(temp_url) == "wprjISNzhzsBHwSVKjMbvHEOqOchMhJX"

    @mark.django_db
    def test_create_batch_temp_url(self, temp_url_factory: TempUrl):
        temp_url_factory.create_batch(20)
        count = TempUrl.objects.all().count()
        assert count == 20
