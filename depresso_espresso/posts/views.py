from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class PostView(TemplateView):
    template_name = "posts/posts.html"

    def get(self, request):
        return render(request, "dist/index.html")

  
def index(request):
    rend = PostView().get(request)
    return rend
