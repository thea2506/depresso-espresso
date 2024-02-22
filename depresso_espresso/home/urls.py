from . import views
from django.urls import path


urlpatterns = [
    path('home', views.stream, name="home"),
]
