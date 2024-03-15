from . import views
from django.urls import path

urlpatterns = [

    # authors
    path('authors/', views.get_authors, name = 'get_authors'),
    path('espresso-api/authors/<str:authorid>', views.author_profile, name ='author_profile'),

    # followers
    path('authors/<str:authorid>/followers/', views.get_followers, name ='get_followers'),
    path('authors/<str:authorid>/followers/<str:foreignid>', views.foreign_author_follow, name='remove follower/ add follower/ check if follower'),
    path('authors/create_follow_request/to/<str:foreignid>', views.create_follow_request, name='create_follow_request'),
    path('respond_to_follow_request/from/<str:foreignid>', views.respond_to_follow_request, name='respond_to_follow_request'),



    path('authors/<str:authorid>', views.front_end, name ='frontend'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('authors/images/<str:image_file>', views.get_image, name='image_file'),
    path('check_follow_status/', views.check_follow_status, name='check_follow_request'),
    path("authors/<str:authorid>/inbox", views.front_end_inbox, name="front_end_inbox"),
]