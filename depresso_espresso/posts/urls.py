from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("new_post/", views.new_post, name="make_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("get_all_posts/", views.get_all_posts, name="get_all_posts"),
    path("authors/<str:authorid>/posts/<str:postid>/toggle_like", views.toggle_like, name="toggle_like"),
    path("authors/<str:authorid>/posts", views.get_author_posts, name="get_author_posts"),
    
    path("authors/<str:authorid>/posts/<str:postid>", views.frontend_explorer, name="post_frontend"),
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>', views.author_post, name ='author_post'),
    
    path("authors/<str:authorid>/posts/<str:postid>/comments", views.get_post_comments, name="get_post_comments"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>", views.get_post_comment, name="get_post_comment"),
    path("make_comment", views.make_comment, name="make_comment"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("delete_comment", views.delete_comment, name="delete_comment"),
    path("authors/<str:authorid>/posts/<str:postid>/share_post", views.share_post, name="share_post"),
    path("authors/<str:authorid>/posts/<str:postid>/likes", views.get_post_likes, name="get_post_likes"),
    # explorer
    path("discover", views.frontend_explorer, name="frontend_explorer"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)