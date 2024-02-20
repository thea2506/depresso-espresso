from . import views
from django.urls import path


urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('user_data', views.user_data, name="user_data")
]
