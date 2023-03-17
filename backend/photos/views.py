import os

from django.conf import settings
from django.http import FileResponse, HttpRequest
from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Image, TempUrl
from .serializers import ImageSerializer


class ImageAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    """Image API View"""

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all the images for the current user
        """
        user = self.request.user
        return (
            Image.objects.select_related("user")
            .filter(user=user)
            .order_by("-timestamp")
        )

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.tier is None:
            return Response(
                {"message": "User has no tier. Get a tier in order to upload images!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.tier is None:
            return Response(
                {"message": "User has no tier. Get a tier in order to upload images!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return self.create(request, *args, **kwargs)


class TempUrlRetrieve(generics.RetrieveAPIView):
    """Returns a static image from a expiring url"""

    def get(self, request: HttpRequest, token: str, *args, **kwargs):
        temp_url = TempUrl.objects.filter(
            expiration_date__gte=timezone.now(), token=token
        ).first()
        if temp_url:
            temp_image = str(temp_url.image)
            temp_image = temp_image[1:]
            path = os.path.join(settings.BASE_DIR, temp_image)
            image_file = open(path, "rb")
            return FileResponse(image_file)
        return Response(
            {"message": "The link you followed has expired or does not exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )
