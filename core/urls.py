from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("", include("dashboard.urls")),
    path("cart/", include("carts.urls")),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
