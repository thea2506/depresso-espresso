from django.urls import path
import inbox.views as views

urlpatterns = [
    path('api/authors/<str:author_id>/inbox',
         views.api_inbox, name='api_inbox'),
]
