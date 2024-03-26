from . import views
from django.urls import path

urlpatterns = [
    path('api/auth/signup', views.register, name="signup"),
    path('api/auth/signin', views.loginUser, name="signin"),
    path("api/auth/logout", views.logoutUser, name="logoutUser"),
    path("api/auth/curUser", views.curUser, name="curUser"),
]
