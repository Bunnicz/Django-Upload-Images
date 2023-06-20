from django.urls import path

from .views import ImageAPIView, TempUrlRetrieve

app_name = "photos"

urlpatterns = [
    path("", ImageAPIView.as_view(), name="images"),
    path("temp/<str:token>", TempUrlRetrieve.as_view(), name="temp-url"),
]
