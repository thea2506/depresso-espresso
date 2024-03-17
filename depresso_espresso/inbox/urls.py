from . import views
from django.urls import path

urlpatterns = [
    path('authors/<str:authorid>/espresso-api/inbox', views.handle_inbox, name="handle_inbox"),
    path('create_notification', views.create_notification, name="signup"),
    path('get_notifications/<str:authorid>', views.get_notifications, name="get_notifications"),
    ]