from . import views
from django.urls import path


urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('user_data', views.user_data, name="user_data"),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('service/authors/<str:author_id>/',views.author_profile, name='author_profile')

]
