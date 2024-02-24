# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Posts
from django.http import JsonResponse
from django import forms
import datetime
# Create your views here.


class PostView(forms.ModelForm):
    template_name = "posts/posts.html"

    def get(self, request):
        return render(request, "dist/index.html")
    class Meta:
        model = Posts
        fields = ("content", "image_url", "visibility")
  
def make_post(request):
    print(request)
    data ={}
    if request.method == 'POST':
        form = PostView(request.POST)
        
        if form.is_valid():  
            post = form.save(commit=False)
            post.content = form.cleaned_data["content"]
            post.image_url = form.cleaned_data["image_url"]
            post.authorid = request.user
            post.publishdate = datetime.datetime.now()
            post.visibility = form.cleaned_data["visibility"]
            

            form.save(commit = True)
            data["post_id"] = post.postid
            data['success'] = True  
            print("great success")
            return JsonResponse(data) 
        else:
            data['success'] = False  
            return JsonResponse(data) 

    rend = PostView().get(request)
    return rend


