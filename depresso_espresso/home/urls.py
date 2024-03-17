from . import views
from django.urls import path


urlpatterns = [
    path('authors/<str:authorid>/espresso-api/inbox', views.handle_inbox, name="handle_inbox"),
    path('home', views.StreamView.as_view(), name="home")
   
    
]
