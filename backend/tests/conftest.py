from factory.django import ImageField
from pytest import fixture, mark
from pytest_factoryboy import register
from rest_framework.test import APIClient

from accounts.models import CustomUser, UserTier
from photos.models import Image
from tests.factories import (
    CustomUserFactory,
    ImageFactory,
    TempUrlFactory,
    UserTierFactory,
)

register(UserTierFactory)
register(CustomUserFactory)
register(ImageFactory)
register(TempUrlFactory)


@fixture
def api_client() -> APIClient:
    """Return APIClient"""
    return APIClient


@fixture
def create_standard_tiers(user_tier_factory: callable) -> list[UserTier]:
    tier_enterprise = user_tier_factory.build(
        id="5244822e-0a70-441e-a33f-d03b5de892ef",
        name="Enterprise",
        img_px200=True,
        img_px400=True,
        img_native=True,
        generated_url=True,
    )
    tier_premium = user_tier_factory.build(
        id="9452ef0d-3a41-4e0c-b078-cdce187de42f",
        name="Premium",
        img_px200=True,
        img_px400=True,
        img_native=True,
        generated_url=False,
    )
    tier_deluxe = user_tier_factory.build(
        id="9a5e4a41-3fbe-4d17-af57-d54641b7e622",
        name="Deluxe",
        img_px200=True,
        img_px400=True,
        img_native=False,
        generated_url=False,
    )
    tier_basic = user_tier_factory.build(
        id="83efa699-590b-4282-b7ef-aa4135e9614f",
        name="Basic",
        img_px200=True,
        img_px400=False,
        img_native=False,
        generated_url=False,
    )
    tiers = [tier_enterprise, tier_premium, tier_deluxe, tier_basic]
    return tiers


@fixture
def test_image_jpeg(image_factory: callable) -> Image:
    return image_factory.build(
        id="5223822e-0a70-441e-a33f-d03b5de892ef",
        image=ImageField(filename="test_image", format="JPEG"),
    )


@fixture
def test_image_gif(image_factory: callable) -> Image:
    return image_factory.build(
        id="5223822e-0a70-441e-a33f-d03b5de892ef",
        image=ImageField(filename="test_image", format="GIF"),
    )


@fixture
def test_image_png(image_factory: callable) -> Image:
    return image_factory.build(
        id="5223822e-0a70-441e-a33f-d03b5de892ef",
        image=ImageField(filename="test_image", format="PNG"),
    )


@fixture
@mark.django_db
def authenticated_user_enterprise(
    api_client: APIClient,
    custom_user_factory: callable,
    create_standard_tiers: list[UserTier],
) -> CustomUser:
    user = custom_user_factory.build(
        id="5223822e-0a70-441e-a33f-d03b5de892ef",
        username="APIUser",
        password="APIuserPass123",
        tier=create_standard_tiers[0],
    )
    client = api_client
    client.force_authenticate(user=user)
    return user
