from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.register, name="signup"),
    path('signin', views.loginview, name = "signin"),
    path('get_auth', views.get_auth, name = "get_auth")

]
