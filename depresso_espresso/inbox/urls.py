from . import views
from django.urls import path

urlpatterns = [
    path('authors/<str:authorid>/espresso-api/inbox', views.handle_inbox, name="handle_inbox"),
    path('create_notification', views.create_notification, name="signup"),
    path('get_notifications/<str:authorid>', views.get_notifications, name="get_notifications"),

    # 1. POST //service/authors/{AUTHOR_ID}/inbox/
    path('espresso-api/authors/<str:authorid>/inbox/', views.post_like_inbox, name ='api_handle_inbox'),
    ]