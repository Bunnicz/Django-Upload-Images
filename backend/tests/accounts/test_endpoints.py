from django.urls import reverse
from pytest import fixture, mark
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import CustomUser, UserTier


@mark.django_db
class TestAccountsEndpoints:
    """Test accounts REST API endpoints"""

    @fixture
    def api_client(self):
        return APIClient()

    @fixture
    def authenticated_user(
        self, custom_user_factory: CustomUser, api_client: APIClient
    ):
        user = custom_user_factory.build()
        client = api_client
        client.force_authenticate(user=user)
        return user

    def test_get_user_tier_list(
        self,
        api_client: APIClient,
        authenticated_user: CustomUser,
        user_tier_factory: UserTier,
    ):
        user_tier_factory.create(
            id="5244822e-0a71-441e-a33f-d03b5de892ef",
            name="Test_Enterprise",
            img_px200=True,
            img_px400=True,
            img_native=True,
            generated_url=True,
        )
        url = reverse("accounts:tiers-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Test_Enterprise"
        assert response.data["results"][0]["img_px200"] == True
        assert response.data["results"][0]["img_px400"] == True
        assert response.data["results"][0]["img_native"] == True
        assert response.data["results"][0]["generated_url"] == True

        api_client.logout()
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )
        assert response.data["detail"].code == "not_authenticated"
