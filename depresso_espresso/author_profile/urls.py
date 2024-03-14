from . import views
from django.urls import path

from posts import views as post_views


urlpatterns = [

    # authors
    path('authors/', views.get_authors, name = 'get_authors'),
    path('authors/<str:authorid>', views.author_profile, name ='author_profile'),

    # followers
    path('authors/<str:authorid>/followers/', views.get_followers, name ='get_followers'),
    path('authors/<str:authorid>/followers/<str:foreignid>', views.foreign_author_follow, name='remove follower/ add follower/ check if follower'),
    path('authors/create_follow_request/from/<str:authorid>/to/<str:foreignid>', views.create_follow_request, name='create_follow_request'),
    path('respond_to_follow_request/from/<str:foreignid>/to/<str:authorid>', views.respond_to_follow_request, name='respond_to_follow_request'),



    path('authors/<str:authorid>', views.front_end, name ='frontend'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('get_author_posts', post_views.get_author_posts, name='author_posts'),
    path('authors/images/<str:image_file>', views.get_image, name='image_file'),
    path('check_follow_status/', views.check_follow_status, name='check_follow_request'),
    path("authors/<str:authorid>/inbox", views.front_end_inbox, name="front_end_inbox"),
    path("get_follow_requests", views.get_follow_requests, name="get_follow_requests"),
]