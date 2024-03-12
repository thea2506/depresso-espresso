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
    path('authors/<str:authorid>/edit_profile', views.edit_profile, name='edit_profile'),

    # Follow/Unfollow functionality
    path('send_follow_request/<str:authorid>', views.send_follow_request, name='send_follow_request'),
    path('respond_to_follow_request', views.respond_to_follow_request, name='respond_to_follow_request'),
    path('authors/<str:authorid>/get_followers', views.get_followers, name='get_followers'),
    path('unfollow/<str:authorid>', views.unfollow, name='unfollow'),

    path('check_follow_status', views.check_follow_status, name='check_follow_request'),
    path("authors/<str:authorid>/inbox", views.front_end_inbox, name="front_end_inbox"),
    path("get_follow_requests", views.get_follow_requests, name="get_follow_requests"),
]