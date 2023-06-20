from django.urls import reverse
from pytest import fixture, mark
from rest_framework import status
from rest_framework.test import APIClient


@mark.django_db
class TestCustomUser:
    """Test accounts endpoints"""

    @fixture
    def api_client(self):
        return APIClient()

    @fixture
    def authenticated_user(self, custom_user_factory, api_client):
        user = custom_user_factory.build()
        client = api_client
        client.force_authenticate(user=user)
        return user

    # @fixture
    # def example_tier(self, user_tier_factory):
    #     return user_tier_factory.build()

    def test_custom_user_model_list(
        self, api_client, authenticated_user, user_tier_factory
    ):
        user_tier_factory.create_batch(4)
        url = reverse("accounts:tiers-list")
        response = api_client.get(url)
        # print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 4
        api_client.logout()
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
