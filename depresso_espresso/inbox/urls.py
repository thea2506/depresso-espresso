from . import views
from django.urls import path

urlpatterns = [
    path('create_notification', views.create_notification, name="signup"),
    path('get_notifications/<str:authorid>', views.get_notifications, name="get_notifications"),
    ]