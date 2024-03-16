from . import views
from django.urls import path


urlpatterns = [
    path('home', views.StreamView.as_view(), name="home"),
    path('/authors/<str:authorid>/inbox', views.handle_inbox, name="inbox")
    
]
