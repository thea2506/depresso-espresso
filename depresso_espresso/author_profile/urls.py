from . import views
from django.urls import path


urlpatterns = [
    path('api/authors/<str:authorid>', views.get_profile, name ='get_profile'),
    path('authors', views.get_authors, name ='get_authors'),
    path('user_data', views.user_data, name="user_data"),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
