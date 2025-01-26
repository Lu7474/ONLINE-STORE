from django.urls import path

from . import views


urlpatterns = [
    path("create-order/", views.CreateOrderView.as_view(), name="create_order"),
]
