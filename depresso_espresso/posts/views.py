# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Post
from .models import Comment
from django.http import JsonResponse
from django import forms
import datetime
from django.db.models import F
from django.utils.timezone import make_aware
from django.core import serializers
import json
# Create your views here.


class PostView(forms.ModelForm):
    template_name = "posts/posts.html"

    def get(self, request):
        return render(request, "dist/index.html")
    class Meta:
        model = Post
        fields = ("content", "image_url", "visibility", "contenttype")

class CommentView(forms.ModelForm):
    template_name = "comments/comments.html"

    def get(self, request):
        return render(request, "dist/index.html")
    class Meta:
        model = Comment
        fields = ("comment", "postid")
  
def make_post(request):
    data ={}
    print(request)
    if request.method == 'POST':
        form = PostView(request.POST)
        
        if form.is_valid():  
            post = form.save(commit=False)
            post.content = form.cleaned_data["content"]
            post.image_url = form.cleaned_data["image_url"]
            post.contenttype = form.cleaned_data["contenttype"]
            post.authorid = request.user
            naive_datetime = datetime.datetime.now()
            post.publishdate = make_aware(naive_datetime)
            post.commentcount = 0
           
            post.authorname = request.user.display_name
            post.visibility = form.cleaned_data["visibility"]

            form.save(commit = True)
            data['success'] = True  
            print("great success")
            post.save()
            return JsonResponse(data) 
        else:
            data['success'] = False  
            return JsonResponse(data) 

    rend = PostView().get(request)
    return rend


def get_all_posts(request):
  posts = Post.objects.all()
  data = serializers.serialize('json', posts)
  print('data', data)
  return HttpResponse(data, content_type='application/json')

def get_author_posts(request):
  print('request')
  print('request', request.user)
  posts = Post.objects.filter(authorid=request.user)
  print(posts)
  data = serializers.serialize('json', posts)
  print('data', data)
  return HttpResponse(data, content_type='application/json')


def toggle_like(request):
  data = json.loads(request.body)
  postid = data.get('postid')
  
  post = Post.objects.get(pk=postid)
 
  if request.user in post.liked_by.all():
    post.liked_by.remove(request.user)
  else:
    post.liked_by.add(request.user)

  post.save()
  return HttpResponse("Success")

def make_comment(request):
    data ={}
    print("Comment request", request)
    if request.method == 'POST':
        form = CommentView(request.POST)
        
        if form.is_valid():  
            comment = form.save(commit=False)
            comment.comment = form.cleaned_data["comment"]
            comment.authorid = request.user
            naive_datetime = datetime.datetime.now()
            comment.publishdate = make_aware(naive_datetime)
            comment.authorname = request.user.display_name

            post = form.cleaned_data.get("postid")
            comment.postid = post
            post.commentcount = F('commentcount') + 1
            post.save()

            form.save(commit = True)
            data['success'] = True  
            print("great success")
            comment.save()
            return JsonResponse(data) 
        else:
            data['success'] = False  
            return JsonResponse(data) 

    rend = CommentView().get(request)
    return rend

def get_post_comments(request):
  print('request', request.user)

  data = json.loads(request.body)
  postid = data.get('postid')
  comments = Comment.objects.filter(postid=postid)
  print(comments)
  data = serializers.serialize('json', comments)
  print('data', data)

  return HttpResponse(data, content_type='application/json')