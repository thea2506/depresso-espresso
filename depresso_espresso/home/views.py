from django.shortcuts import render
from .userstream import StreamView
from .search import SearchView
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView


class StreamView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, "dist/index.html")



# Create your views here.
"""
@login_required
def stream(request):
    '''Shows the user their stream page'''
    StreamView()
    return render(request, "dist/index.html" )

@login_required
def search(request):
    '''Shows the user their search results for other users'''
    SearchView()
    return render(request, "dist/index.html")
    

    
"""



