from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("users/", include("users.urls")),
    # path("users/", include("django.contrib.auth.urls")),
    path("", include("dashboard.urls")),
]

if DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
