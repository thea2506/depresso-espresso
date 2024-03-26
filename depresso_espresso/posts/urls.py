from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/authors/<str:author_id>/posts/',
         views.api_posts, name='api_posts'),
    path('api/authors/<str:author_id>/posts/<str:post_id>',
         views.api_post, name='api_post'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/image/',
         views.api_get_image, name='api_post'),
    path('api/authors/<str:author_id>/posts/<str:post_id>/comments/',
         views.api_comments, name='api_comments'),
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
