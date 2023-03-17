from rest_framework import permissions, viewsets

from .models import CustomUser, UserTier
from .serializers import UserSerializer, UserTierSerializer  # GroupSerializer,


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user tiers to be viewed or edited.
    """

    queryset = UserTier.objects.all().order_by("name")
    serializer_class = UserTierSerializer
    permission_classes = [permissions.IsAuthenticated]
