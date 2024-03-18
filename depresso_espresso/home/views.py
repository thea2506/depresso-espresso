from django.shortcuts import render
from .userstream import StreamView
from .search import SearchView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from authentication.models import Author, Following, FollowRequest, Node
from posts.models import Post
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core import serializers



class StreamView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, "index.html")

# Create your views here.

def stream(request):
    rend = StreamView().get(request)
    return rend




