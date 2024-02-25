from django.urls import path
from . import views

urlpatterns = [
    path("make_post", views.make_post, name="make_post"),
    path("get_all_posts", views.get_all_posts, name="get_all_posts"),
    path("like_post", views.like_post, name="like_post"),
]