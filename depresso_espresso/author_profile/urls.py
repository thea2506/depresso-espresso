from . import views
from django.urls import path

from posts import views as post_views


urlpatterns = [
    path('api/authors/<str:authorid>', views.get_profile, name ='get_profile'),
    path('authors/<str:authorid>', views.front_end, name ='frontend'),
    path('authors', views.get_authors, name ='get_authors'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('get_author_posts', post_views.get_author_posts, name='author_posts'),
    path('authors/images/<str:image_file>', views.get_image, name='image_file'),
    path('edit_profile/<str:authorid>', views.edit_profile, name='edit_profile'),
]