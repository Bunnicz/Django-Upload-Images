# import json

# import pytest

# pytestmark = pytest.mark.django_db


# class TestCustomUserEndpoints:
#     endpoint = "/api/users"

#     def test_custom_users_get(self, custom_user_factory, api_client):
#         # custom_user_factory.create_batch(4)
#         custom_user_factory()
#         print(custom_user_factory.username, custom_user_factory.password)
#         api_client().login(
#             username=custom_user_factory.username, password=custom_user_factory.password
#         )
#         response = api_client().get(self.endpoint)
#         print(response)
#         assert response.status_code == 200
#         assert len(json.loads(response.content)) == 1


# class TestUserTiersEndpoints:
#     endpoint = "/api/tiers"

#     def test_user_tiers_get(self, user_tier_factory, api_client):
#         # custom_user_factory.create_batch(4)
#         user_tier_factory()

#         response = api_client().get(self.endpoint)
#         print(response)
#         assert response.status_code == 200
#         assert len(json.loads(response.content)) == 1
