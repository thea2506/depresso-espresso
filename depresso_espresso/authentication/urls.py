from . import views
from django.urls import path

urlpatterns = [
    path('auth/signup', views.register, name="signup"),
    path('auth/signin', views.loginUser, name="signin"),
    path("auth/logout", views.logoutUser, name="logoutUser"),
    path("auth/curUser", views.curUser, name="curUser"),
]
