from django.urls import path
from . import views

urlpatterns = [
    path("make_post", views.make_post, name="make_post"),
    path("get_all_posts", views.get_all_posts, name="get_all_posts"),
    path("toggle_like", views.toggle_like, name="toggle_like"),
    path("get_author_posts", views.get_author_posts, name="get_author_posts"),
]