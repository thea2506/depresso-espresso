from django.urls import path
from . import views

urlpatterns = [
    path("make_post", views.make_post, name="make_post"),
]