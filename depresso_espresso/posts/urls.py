from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("make_post", views.make_post, name="make_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("get_all_posts", views.get_all_posts, name="get_all_posts"),
    path("toggle_like", views.toggle_like, name="toggle_like"),
    path("get_author_posts", views.get_author_posts, name="get_author_posts"),
    path("make_comment", views.make_comment, name="make_comment"),
    path("get_post_comments", views.get_post_comments, name="get_post_comments"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("delete_comment", views.delete_comment, name="delete_comment"),
    path("share_post", views.share_post, name="share_post"),

    # explorer
    path("discover", views.frontend_explorer, name="frontend_explorer"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)