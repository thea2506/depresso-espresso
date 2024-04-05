from django.urls import path
from . import views

urlpatterns = [
    path('api/authors/<str:author_id>/posts/',
         views.api_posts, name='api_posts'),
    path('api/authors/<str:author_id>/posts',
         views.api_posts, name='api_posts_paginated'),
    path('api/authors/<str:author_id>/posts/<str:post_id>',
         views.api_post, name='api_post'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/image',
         views.api_get_image, name='api_get_image'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/comments',
         views.api_comments, name='api_comments'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/likes',
         views.api_post_like, name='api_post_like'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes',
         views.api_comment_like, name='api_comment_like'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/like',
         views.api_likes, name='api_likes'),
     path('api/posts',
          views.api_get_public_posts, name='api_get_public_posts'),

    # FRONTEND URLS
    path("api/execute", views.api_execute, name="api_execute"),
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
