from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Creating stuff
    path("new_post/", views.new_local_post, name="new_local__post"),
    path("new_external_post/", views.new_external_post, name="new_external__post"),
    path("make_comment", views.make_comment, name="make_comment"),
    path("authors/<str:authorid>/posts/<str:postid>/share_post", views.share_post, name="share_post"),
    path("authors/<str:authorid>/posts/<str:postid>/like_post", views.like_post, name="like_post"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>/like_comment", views.like_comment, name="like_comment"),

    # Getting stuff
    path("get_all_posts/", views.get_all_posts, name="get_all_posts"),
    path("authors/<str:authorid>/liked", views.get_author_liked, name="get_author_liked"),
    path("authors/<str:authorid>/posts", views.get_author_posts, name="get_author_posts"),
    
    path("authors/<str:authorid>/posts/<str:postid>", views.frontend_explorer, name="post_frontend"),
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>', views.author_post, name ='author_post'),
    
    path("authors/<str:authorid>/posts/<str:postid>", views.author_post, name="author_post"),
    path("authors/<str:authorid>/posts/<str:postid>/likes", views.get_post_likes, name="get_post_likes"),
    path("authors/<str:authorid>/posts/<str:postid>/comments", views.get_post_comments, name="get_post_comments"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>", views.get_post_comment, name="get_post_comment"),
    
    # Modifying stuff
    path("delete_post", views.delete_post, name="delete_post"),
    path("delete_comment", views.delete_comment, name="delete_comment"),
    path("edit_post", views.edit_post, name="edit_post"),

    # explorer
    path("discover", views.frontend_explorer, name="frontend_explorer"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)