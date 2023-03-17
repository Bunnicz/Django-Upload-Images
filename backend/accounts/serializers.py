# from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import CustomUser, UserTier


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["url", "username", "tier"]


class UserTierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserTier
        fields = ["name", "img_px200", "img_px400", "img_native", "generated_url"]
