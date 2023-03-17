from django.urls import path

from .views import ImageAPIView, TempUrlRetrieve

urlpatterns = [
    path("", ImageAPIView.as_view()),
    path("temp/<str:token>", TempUrlRetrieve.as_view(), name="temp-url"),
]
