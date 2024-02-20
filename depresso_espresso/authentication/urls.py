from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.register, name="signun"),
    path('signin', views.loginview, name = "signin")
]
