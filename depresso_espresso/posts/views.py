# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .models import Comment
from authentication.models import Author
from django.http import JsonResponse
from django import forms
import datetime
from django.db.models import F
from django.utils.timezone import make_aware
from django.core import serializers
import json
from django.shortcuts import get_object_or_404
# Create your views here.


class PostView(forms.ModelForm):
    template_name = "posts/posts.html"

    def get(self, request):
        return render(request, "index.html")
    class Meta:
        model = Post
        # all_fields = ("type", "title", "id", "published", "visibility", "source", "origin", "author", "description", "contentType", "content", "count", "comments", "liked_by")
        fields = ("title", "visibility", "description", "contentType", "content")

class CommentView(forms.ModelForm):
    template_name = "comments/comments.html"

    def get(self, request):
        return render(request, "index.html")
    class Meta:
        model = Comment
        fields = ("comment", "postid")
  
def make_post(request):
    data ={}
    if request.method == 'POST':  
        form = PostView(request.POST)
      
        if form.is_valid():
          post = form.save(commit=False)
          
          post.type = "post"
          post.title = form.cleaned_data["title"]
          post.description = form.cleaned_data["description"]
          post.contentType = form.cleaned_data["contentType"]
          post.content = form.cleaned_data["content"]
          post.author = request.user
          post.visibility = form.cleaned_data["visibility"]
          post.published = make_aware(datetime.datetime.now())

          # images
          form.save(commit = True)
          data['success'] = True  
          post.save()
          return JsonResponse(data) 
        else:
          print("form is not valid", form.errors)
          data['success'] = False  
        return JsonResponse(data) 

    return render(request, "index.html")

def get_all_posts(request):
  posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')
  authors = [Author.objects.get(id=(post.author.id)) for post in posts]
  data = serializers.serialize('json', posts)
  author_data = serializers.serialize('json', authors, fields=["id", "profileImage", "displayName", "github", "displayName"])
  results = '{"posts": ', data, ', "authors": ', author_data, '}'
  return HttpResponse(results, content_type='application/json')

def get_author_posts(request):
  author_id = request.GET.get('authorid')
  author = [Author.objects.get(id=author_id)]
  posts = Post.objects.filter(author=author[0]).order_by('-published')
  data = serializers.serialize('json', posts)
  author_data = serializers.serialize('json', author, fields=["id", "profileImage", "displayName", "github", "displayName"])

  results = '{"posts": ', data, ', "authors": ', author_data, '}'
  return HttpResponse(results, content_type='application/json')

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
    if request.method == 'POST':
        form = CommentView(request.POST)
        
        if form.is_valid():  
            comment = form.save(commit=False)
            comment.comment = form.cleaned_data["comment"]
            comment.authorid = request.user
            naive_datetime = datetime.datetime.now()
            comment.publishdate = make_aware(naive_datetime)
            comment.authorname = request.user.displayName

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
  '''Get all comments for a post'''
  print('request', request.user)

  data = json.loads(request.body)
  postid = data.get('postId')
  comments = Comment.objects.filter(postid=postid)
  commentData = serializers.serialize('json', comments)
  authorData = []
  for comment in comments:
    author = Author.objects.get(username=(comment.authorid))
    authorData.append(author)
  authorData = serializers.serialize("json", authorData, fields=["id", "profileImage", "displayName", "github", "displayName"])

  list_a = json.loads(commentData)
  list_b = json.loads(authorData)
  merged = {"author": list_b, "comment": list_a}
  data = json.dumps(merged)

  return HttpResponse(data, content_type='application/json')

def delete_post(request):
  '''Delete a post'''
  data = {}

  data = json.loads(request.body)
  postid = data.get('postid')
  post = Post.objects.get(pk=postid)

  if request.user == post.author:
    post.delete()
    data['success'] = True  
    print("great deletion success")
    return JsonResponse(data) 
  
  else:
    data['success'] = False
    print("horrible deletion failure")
    return JsonResponse(data)

def delete_comment(request):
  '''Delete a comment'''
  data = {}

  data = json.loads(request.body)
  commentid = data.get('commentid')
  comment = Comment.objects.filter(commentid=commentid)
  print('request', request.user, 'comment', comment)

  if request.user == comment.authorid.user:
    comment.delete()
    data['success'] = True  
    print("great deletion success")
    return JsonResponse(data) 
  
  else:
    data['success'] = False
    print("horrible deletion failure")
    return JsonResponse(data)
  
def edit_post(request):
  data = {}
  postid = request.POST.get('postid') 

  post = get_object_or_404(Post, pk=postid)
  if request.method == 'POST':
      post.content = request.POST.get('content')
      post.visibility = request.POST.get('visibility')
      post.contentType = request.POST.get('contenttype')
      post.save()
  data['success'] = True
  return JsonResponse(data)