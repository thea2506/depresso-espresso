from . import views
from django.urls import path


urlpatterns = [
    path('home', views.StreamView.as_view(), name="home")
   
    
]
