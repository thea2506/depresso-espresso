from . import views
from django.urls import path


urlpatterns = [
    path('profile', views.profile, name="profile")
]
