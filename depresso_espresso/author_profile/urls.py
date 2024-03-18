from . import views
from django.urls import path

urlpatterns = [

    # authors
    path('authors', views.get_authors, name = 'get_authors'),
    path('authors/<str:authorid>', views.front_end, name ='frontend'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('authors/images/<str:image_file>', views.get_image, name='image_file'),
    path("authors/<str:authorid>/inbox", views.front_end_inbox, name="front_end_inbox"),
    path("get_follow_requests", views.get_follow_requests, name="get_follow_requests"),

    # followers
    path('authors/<str:authorid>/followers/', views.get_followers, name ='get_followers'),
    path('authors/<str:authorid>/followers/<str:foreignid>', views.handle_follow, name='remove follower/ add follower/ check if follower'),
    path('authors/create_follow_request/to/<str:foreignid>', views.create_follow_request, name='create_follow_request'),
    path('authors/create_external_follow_request/', views.create_external_follow_request, name='create_follow_request'),
    path('respond_to_follow_request/from/<str:foreignid>', views.respond_to_follow_request, name='respond_to_follow_request'),
    path('authors/<str:authorid>/friends/', views.get_friends, name = 'get_friends'),
    path('authors/<str:authorid>/following/', views.get_followers, name = 'get_following'),
    path('check_follow_status/', views.check_follow_status, name='check_follow_request'),
    path('get_follow_list', views.get_follow_list, name='get_follow_list'),

    # REQUIRED API ENDPOINTS
    # 1. GET //service/authors/ - Parameters: page, size
    path('espresso-api/authors', views.api_get_authors, name='api_get_authors'),
    
    # 2. GET //service/authors/{AUTHOR_ID}/
    path('espresso-api/authors/<str:authorid>', views.author_profile, name ='author_profile'),

    # 3. GET //service/authors/{AUTHOR_ID}/followers
    path('espresso-api/authors/<str:authorid>/followers', views.get_followers, name='api_get_followers'),

    # 4. GET/DELETE/PUT //service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    path('espresso-api/authors/<str:authorid>/followers/<str:foreignid>', views.handle_follow, name='api_handle_follow'),
]