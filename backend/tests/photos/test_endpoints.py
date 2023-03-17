# import uuid

# import pytest

# pytestmark = pytest.mark.django_db


# class TestImageEndpoints:
#     endpoint = "/api/images"

#     # def __init__(self):

#     def test_image_get(
#         self, image_factory, user_tier_factory, custom_user_factory, api_client
#     ):
#         image_factory()
#         tier = user_tier_factory(
#             id=uuid.uuid4(),
#             name="Enterprise",
#             img_px200=True,
#             img_px400=True,
#             img_native=True,
#             generated_url=True,
#         )
#         custom_user_factory(username="TestEnterprise", password="password", tier=tier)
#         print(custom_user_factory.username, custom_user_factory.password)
#         api_client().login(
#             username=custom_user_factory.username, password=custom_user_factory.password
#         )
#         response = api_client().get(self.endpoint, follow=True)

#         assert response.status_code == 200
