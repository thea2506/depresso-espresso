from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Creating stuff
    path("make_comment", views.make_comment, name="make_comment"),
    path("authors/<str:authorid>/posts/<str:postid>/share_post", views.share_post, name="share_post"),
    path("authors/<str:authorid>/posts/<str:postid>/like_post", views.like_post, name="like_post"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>/like_comment", views.like_comment, name="like_comment"),

    # Getting stuff
    path("authors/<str:authorid>/liked", views.get_author_liked, name="get_author_liked"),
    path("authors/<str:authorid>/posts/<str:postid>", views.frontend_explorer, name="post_frontend"),
    
    path("authors/<str:authorid>/posts/<str:postid>", views.handle_author_post, name="author_post"),
    path("authors/<str:authorid>/posts/<str:postid>/likes", views.get_post_likes, name="get_post_likes"),
    path("authors/<str:authorid>/posts/<str:postid>/comments", views.get_post_comments, name="get_post_comments"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>", views.get_post_comment, name="get_post_comment"),
    
    # Modifying stuff
    path("delete_comment", views.delete_comment, name="delete_comment"),

    # explorer
    path("discover", views.frontend_explorer, name="frontend_explorer"),


    # REQUIRED API ENDPOINTS (Post Covered)
    # 1. GET/DELETE/PUT //service/authors/{AUTHOR_ID}/posts/{POST_ID}
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>', views.handle_author_post, name ='author_post'),

    # 2. GET/POST //service/authors/{AUTHOR_ID}/posts - parameter: page, size
    path('espresso-api/authors/<str:authorid>/posts/', views.api_posts, name ='api_get_posts'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)