from django.shortcuts import render
from .userstream import StreamView
from .search import SearchView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class StreamView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, "index.html")

@login_required
def stream(request):
    '''Shows the user their stream page'''
    rend = StreamView().get(request)
    return rend


"""
@login_required
def search(request):
    '''Shows the user their search results for other users'''
    SearchView()
    return render(request, "index.html")
    
"""
