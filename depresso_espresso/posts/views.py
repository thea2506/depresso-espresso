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
        fields = ("content", "image_url", "visibility", "contenttype", "image_file")

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
        print("Post request", request.user.displayName)
        form = PostView(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.content = form.cleaned_data["content"]
            post.image_url = form.cleaned_data["image_url"]
            post.contenttype = form.cleaned_data["contenttype"]
            post.authorid = request.user
            naive_datetime = datetime.datetime.now()
            post.publishdate = make_aware(naive_datetime)
            post.commentcount = 0
           
            post.authorname = request.user.displayName
            post.visibility = form.cleaned_data["visibility"]

            # images
            post.image_file = form.cleaned_data["image_file"]
            print("image file add",post.image_file)

            form.save(commit = True)
            data['success'] = True  
            post.save()
            return JsonResponse(data) 
        else:
            print("form is not valid")
            print(form.errors)
            data['success'] = False  
            return JsonResponse(data) 

    return render(request, "index.html")

def get_all_posts(request):
  posts = Post.objects.filter(visibility="public").order_by('-publishdate')
  data_dict = json.loads(serializers.serialize('json', posts))

  for model in data_dict:
     print("MODELLLLLLL: ", model)
     author_of_post = Author.objects.filter(authorid = model["fields"]["authorid"])
     author_of_post_json = json.loads(serializers.serialize('json', author_of_post))
     print("author_of_post_json", author_of_post_json)
     model["fields"]["author_profile_image"] = author_of_post_json[0]["fields"]["profile_image"]
     model["fields"]["author_username"] = author_of_post_json[0]["fields"]["username"]

  return HttpResponse(json.dumps(data_dict), content_type='application/json')

def get_author_posts(request):
  author_id = request.GET.get("id")
  posts = Post.objects.filter(authorid=author_id).order_by('-publishdate')
  data = serializers.serialize('json', posts)
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

  if request.user == post.authorid:
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
      if request.FILES.get('image_file'):
        post.image_file = request.FILES.get('image_file')
      post.content = request.POST.get('content')
      post.image_url = request.POST.get('image_url')
      post.visibility = request.POST.get('visibility')
      post.contenttype = request.POST.get('contenttype')
      post.save()
  data['success'] = True
  return JsonResponse(data)