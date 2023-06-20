from django.urls import include, path
from rest_framework import routers

from .views import UserTierViewSet, UserViewSet

app_name = "accounts"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tiers", UserTierViewSet, basename="tiers")

urlpatterns = [
    path("", include(router.urls)),
]
