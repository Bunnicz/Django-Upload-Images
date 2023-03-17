from django.urls import include, path
from rest_framework import routers

from .views import UserTierViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"tiers", UserTierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
