from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('posts', views.api_posts, name='api_posts'),
    path('posts/<str:post_id>', views.api_post, name='api_posts'),
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
