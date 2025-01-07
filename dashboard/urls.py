from django.urls import path

from .views import (
    index,
)

urlpatterns = [
    path("", index, name="index"),
#     path("categories", category_view, name="category_view"),
]
