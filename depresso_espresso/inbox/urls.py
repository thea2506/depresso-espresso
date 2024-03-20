from . import views
from django.urls import path

urlpatterns = [

    # 1. GET/POST //service/authors/{AUTHOR_ID}/inbox/
    path('espresso-api/authors/<str:authorid>/inbox',
         views.api_inbox, name='api_inbox'),
]
