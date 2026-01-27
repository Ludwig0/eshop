from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("mine/", views.my_orders, name="my_orders"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
]
