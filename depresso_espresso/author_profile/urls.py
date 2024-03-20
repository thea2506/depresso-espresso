from . import views
from django.urls import path

urlpatterns = [

    # authors
    path('authors', views.get_authors, name='get_authors'),
    path('authors/<str:authorid>', views.front_end, name='frontend'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('authors/images/<str:image_file>',
         views.get_image, name='image_file'),
    path("authors/<str:authorid>/inbox",
         views.front_end_inbox, name="front_end_inbox"),
    path("get_follow_requests", views.get_follow_requests,
         name="get_follow_requests"),

    # followers
    path('authors/<str:authorid>/followers/',
         views.api_get_followers, name='get_followers'),
    path('authors/<str:authorid>/followers/<str:foreignid>', views.handle_follow,
         name='handle_follow'),
    # path('authors/create_follow_request/to/<path:foreignid>', views.create_follow_request, name='create_follow_request'),
    path('authors/respond_to_follow_request/from/<path:foreignid>',
         views.respond_to_follow_request, name='respond_to_follow_request'),
    path('authors/<str:authorid>/friends/',
         views.get_friends, name='get_friends'),
    path('authors/<str:authorid>/following/',
         views.api_get_followers, name='get_following'),
    path('check_follow_status/', views.check_follow_status,
         name='check_follow_request'),
    path('get_follow_list', views.get_follow_list, name='get_follow_list'),


    # REQUIRED API ENDPOINTS (Authors, Single Author, Followers, Friend/Follow Request Covered)
    # 1. GET //service/authors/ - Parameters: page, size
    path('espresso-api/authors/', views.api_get_authors, name='api_get_authors'),

    # 2. GET //service/authors/{AUTHOR_ID}/
    path('espresso-api/authors/<str:authorid>',
         views.api_author, name='api_author'),

    # 3. GET //service/authors/{AUTHOR_ID}/followers
    path('espresso-api/authors/<str:authorid>/followers',
         views.api_get_followers, name='api_get_followers'),


    # 4 PUT //service/authors/<str:authorid>/followers/<str:foreignid>
    path('espresso-api/authors/<str:authorid>/followers/<str:foreignid>',
         views.api_add_follower, name='api_add_follower'),

    # 5. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>/likes',
         views.api_get_likes, name='api_get_likes'),

    # 6. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    path('espresso-api/authors/<str:authorid>/posts/<str:postid>/comments/<str:commentid>/likes',
         views.api_get_likes_comment, name='api_get_likes_comment'),

    # 7. GET //service/authors/{AUTHOR_ID}/liked
    path('espresso-api/authors/<str:authorid>/liked',
         views.api_get_author_liked, name='api_get_likes_comment'),
]
