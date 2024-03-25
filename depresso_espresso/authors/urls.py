from . import views
from django.urls import path, include

urlpatterns = [
    path('authors/<str:author_id>', views.api_author, name='authors'),
    path('authors/<str:author_id>/followers',
         views.api_followers, name='authors'),
    path('authors/<str:author_id>/followers/<path:author_url>',
         views.api_follower, name='authors'),
    path('authors/<str:author_id>/liked',
         views.api_liked, name='authors'),
    path('authors/<str:author_id>/', include('posts.urls')),
    path('authors/<str:author_id>/', include('inbox.urls')),
    path('authors/<path:author_url>',
         views.api_external_author, name='external_authors'),
]
