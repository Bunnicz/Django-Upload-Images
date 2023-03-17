from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/images/", include("photos.urls")),
    path("api/", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# http://127.0.0.1:8000/api-auth/login/
# http://127.0.0.1:8000/api-auth/logout/
