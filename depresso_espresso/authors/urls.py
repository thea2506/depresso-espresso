from . import views
from django.urls import path, include

urlpatterns = [
    path('authors/<str:author_id>/', include('posts.urls')),
]
