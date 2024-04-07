from . import views
from django.urls import path

urlpatterns = [
    path('api/discover/', views.api_discover, name='discover'),

    path('api/authors/', views.api_authors, name='authors'),
    path('api/authors', views.api_authors, name='authors'),
    path('api/authors/<str:author_id>/', views.api_author, name='author'),
    path('api/authors/<str:author_id>', views.api_author, name='author'),
    path('api/authors/<str:author_id>/make_friends/<path:author_url>',
         views.api_make_friends, name='author_make_friends'),
    path('api/authors/<str:author_id>/followers',
         views.api_followers, name='authors'),
    path('api/authors/<str:author_id>/followers/<path:author_url>',
         views.api_follower, name='authors'),
    path('api/authors/<str:author_id>/liked/',
         views.api_liked, name='authors'),

    path('api/authors/<str:author_id>/decline',
         views.api_handle_decline, name='handle_decline'),

    path('api/authors/<str:author_id>/send_follow_request/<path:author_url>',
          views.send_follow_request, name='send_follow_request'),
]
