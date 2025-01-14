from django.urls import path

from .views import IndexView, CatalogView, ProductView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("search/", CatalogView.as_view(), name="search"),
    path("<slug:category_slug>/", CatalogView.as_view(), name="index"),
    path("product/<slug:product_slug>/", ProductView.as_view(), name="product"),
]
