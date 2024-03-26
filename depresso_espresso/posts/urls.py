from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/authors/<str:author_id>/posts/',
         views.api_posts, name='api_posts'),
    path('api/authors/<str:author_id>/posts/<str:post_id>',
         views.api_post, name='api_post'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/image',
         views.api_get_image, name='api_get_image'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/comments',
         views.api_comments, name='api_comments'),

    # likes for comments and posts missing
    path('api/authors/<str:author_id>/posts/<str:post_id>/likes',
         views.api_post_like, name='api_post_like'),

    path('api/authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes',
         views.api_comment_like, name='api_comment_like'),
    path('posts/<str:post_id>/likes', views.api_likes, name='api_likes'),
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
