from django.urls import path, include
import inbox.views as views

urlpatterns = [
    path('inbox/', views.api_inbox, name='api_inbox'),
]
