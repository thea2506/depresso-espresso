from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.register, name="signup"),
    path('signin', views.frontend, name = "frontend"),
    path('api/signin', views.loginUser, name = "signin"),
    path("logoutUser", views.logoutUser, name = "logoutUser")
]
