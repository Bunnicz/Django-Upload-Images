from django.utils import timezone
from factory import (Faker, LazyFunction, RelatedFactory, Sequence, SubFactory,
                     Trait)
from factory.django import DjangoModelFactory, ImageField

from accounts.models import CustomUser, UserTier
from photos.models import Image, TempUrl


# ______ACCOUNTS APP______:
class UserTierFactory(DjangoModelFactory):
    class Meta:
        model = UserTier

    id = Faker("uuid4")
    name = Sequence(lambda n: "Tier_{0}".format(n))
    img_px200 = Faker("boolean")
    img_px400 = Faker("boolean")
    img_native = Faker("boolean")
    generated_url = Faker("boolean")


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    id = Faker("uuid4")
    username = Sequence(lambda n: "User_{0}".format(n))
    password = Faker("password")
    tier = None

    class Params:
        with_tier = Trait(tier=SubFactory(UserTierFactory))


# ______PHOTOS APP______:
class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    id = Faker("uuid4")
    image = ImageField()
    user = SubFactory(CustomUserFactory)
    timestamp = LazyFunction(timezone.now)
    delete_url_time = None

    class Params:
        with_delete_url_time = Trait(
            with_temp_url=True, delete_url_time=Faker("random_number", digits=3)
        )
        with_temp_url = Trait(
            temp_url=RelatedFactory("tests.factories.TempUrlFactory"),
        )


class TempUrlFactory(DjangoModelFactory):
    class Meta:
        model = TempUrl

    id = Faker("uuid4")
    image = SubFactory(ImageFactory)
    token = Faker("pystr", max_chars=32)
    expiration_date = LazyFunction(timezone.now)
