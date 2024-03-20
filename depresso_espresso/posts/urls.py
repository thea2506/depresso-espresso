from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Creating stuff
    path("authors/<str:authorid>/posts/<str:postid>/share_post",
         views.share_post, name="share_post"),

    # Getting stuff
    path("authors/<str:authorid>/posts",
         views.get_author_posts, name="get_author_posts"),
    path("authors/<str:authorid>/liked",
         views.get_author_liked, name="get_author_liked"),
    path("authors/<str:authorid>/posts/<str:postid>",
         views.frontend_explorer, name="post_frontend"),

    path("authors/<str:authorid>/posts/<str:postid>",
         views.handle_author_post, name="author_post"),
    path("authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>",
         views.get_post_comment, name="get_post_comment"),

    # Modifying stuff
    path("delete_comment", views.delete_comment, name="delete_comment"),

    # explorer
    path("discover", views.frontend_explorer, name="frontend_explorer"),


    # REQUIRED API ENDPOINTS (Post Covered)
    # 1. GET/DELETE/PUT //service/authors/{AUTHOR_ID}/posts/{POST_ID}
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>',
         views.handle_author_post, name='author_post'),

    # 2. GET/POST //service/authors/{AUTHOR_ID}/posts - parameter: page, size
    path('espresso-api/authors/<str:authorid>/posts/',
         views.api_posts, name='api_get_posts'),

    # 3. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>/image',
         views.api_get_image, name='api_get_image'),

    # 4. GET/POST //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>/comments',
         views.api_get_comments, name='api_get_comments'),

    # 5. GET //service/posts/
    path('espresso-api/posts/',
         views.api_get_feed, name='api_get_feed'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
