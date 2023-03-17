from pytest import mark

from accounts.models import CustomUser, UserTier


class TestCustomUserModel:
    """CustomUser model test cases"""

    def test_build_user_without_tier(self, custom_user_factory: CustomUser):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert not custom_user.tier

    def test_build_user_with_tier(self, custom_user_factory: CustomUser):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
            with_tier=True,
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert custom_user.tier

    def test_build_user_with_basic_tier(
        self, custom_user_factory: CustomUser, create_standard_tiers: list[UserTier]
    ):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
            tier=create_standard_tiers[3],
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert custom_user.tier.name == "Basic"
        assert custom_user.tier.img_px200 is True
        assert custom_user.tier.img_px400 is False
        assert custom_user.tier.img_native is False
        assert custom_user.tier.generated_url is False

    def test_build_user_with_deluxe_tier(
        self, custom_user_factory: CustomUser, create_standard_tiers: list[UserTier]
    ):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
            tier=create_standard_tiers[2],
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert custom_user.tier.name == "Deluxe"
        assert custom_user.tier.img_px200 is True
        assert custom_user.tier.img_px400 is True
        assert custom_user.tier.img_native is False
        assert custom_user.tier.generated_url is False

    def test_build_user_with_premium_tier(
        self, custom_user_factory: CustomUser, create_standard_tiers: list[UserTier]
    ):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
            tier=create_standard_tiers[1],
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert custom_user.tier.name == "Premium"
        assert custom_user.tier.img_px200 is True
        assert custom_user.tier.img_px400 is True
        assert custom_user.tier.img_native is True
        assert custom_user.tier.generated_url is False

    def test_build_user_with_enterprise_tier(
        self, custom_user_factory: CustomUser, create_standard_tiers: list[UserTier]
    ):
        custom_user = custom_user_factory.build(
            id="5223822e-0a70-441e-a33f-d03b5de892ef",
            username="John",
            password="TestMyPassword123",
            tier=create_standard_tiers[0],
        )
        assert custom_user.id == "5223822e-0a70-441e-a33f-d03b5de892ef"
        assert custom_user.username == "John"
        assert custom_user.password == "TestMyPassword123"
        assert custom_user.tier.name == "Enterprise"
        assert custom_user.tier.img_px200 is True
        assert custom_user.tier.img_px400 is True
        assert custom_user.tier.img_native is True
        assert custom_user.tier.generated_url is True

    def test_str_method(
        self, custom_user_factory: CustomUser, user_tier_factory: UserTier
    ):
        test_tier = user_tier_factory.build(name="test_tier")
        user_without_tier = custom_user_factory.build(username="user_without_tier")
        user_with_tier = custom_user_factory.build(
            username="user_with_tier", tier=test_tier
        )

        assert str(user_without_tier) == "user_without_tier-None"
        assert str(user_with_tier) == "user_with_tier-test_tier"

    @mark.django_db
    def test_create_batch_custom_user_without_tier(
        self, custom_user_factory: CustomUser
    ):
        custom_user_factory.create_batch(20)
        count = CustomUser.objects.all().count()
        assert count == 20

    @mark.django_db
    def test_create_batch_custom_user_with_tier(self, custom_user_factory: CustomUser):
        custom_user_factory.create_batch(20, with_tier=True)
        count = CustomUser.objects.all().count()
        count_tiers = CustomUser.objects.filter(tier__name__startswith="Tier_").count()
        assert count == 20
        assert count_tiers == 20


class TestUserTierModel:
    """UserTier model test cases"""

    def test_build_user_tier(self, user_tier_factory: UserTier):
        user_tier = user_tier_factory.build(
            id="5244822e-0a71-441e-a33f-d03b5de892ef",
            name="Test_Enterprise",
            img_px200=True,
            img_px400=True,
            img_native=True,
            generated_url=True,
        )
        assert user_tier.id == "5244822e-0a71-441e-a33f-d03b5de892ef"
        assert user_tier.name == "Test_Enterprise"
        assert user_tier.img_px200 is True
        assert user_tier.img_px400 is True
        assert user_tier.img_native is True
        assert user_tier.generated_url is True

    def test_str_method(self, user_tier_factory: UserTier):
        user_tier = user_tier_factory.build(name="test_name")
        assert str(user_tier) == "test_name"

    @mark.django_db
    def test_create_batch_user_tier(self, user_tier_factory: UserTier):
        user_tier_factory.create_batch(20)
        count = UserTier.objects.all().count()
        assert count == 20
