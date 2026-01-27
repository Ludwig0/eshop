from django.urls import path
from . import views

urlpatterns = [
    path("product/<int:product_id>/review/", views.upsert_review, name="upsert_review"),
]
