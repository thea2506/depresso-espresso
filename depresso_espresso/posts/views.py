# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Comment, LikePost, LikeComment, Share
from authentication.models import Author, Node
from django.http import JsonResponse
from django import forms
import datetime
from django.db.models import F
from rest_framework.decorators import api_view
from django.utils.timezone import make_aware
from django.core import serializers
import json, requests
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session


class PostView(forms.ModelForm):
    template_name = "post/post.html"

    def get(self, request):
        return render(request, "index.html")
    class Meta:
        model = Post
        # fields = ("type", "title", "id", "source", "origin", "description", "contentType", "content", "count", "comments", "published", "visibility")
        fields = ("title", "visibility", "description", "contentType", "content")

class CommentView(forms.ModelForm):
    template_name = "comment/comment.html"

    def get(self, request):
        return render(request, "index.html")
    class Meta:
        model = Comment
        fields = ("comment", "postid")


@api_view(['GET', 'DELETE', 'PUT'])
def author_post(request, authorid, postid):

  if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)
    
      local_author = Author.objects.filter(id = authorid).exists()

  if  not local_author: # if the author of the post is not saved on our server:
      split_id = authorid.split("authors")
      node = Node.objects.get(baseUrl = split_id[0]) # get the host from the id
      username = node["theirUsername"]
      password = node["theirPassword"]
      response = requests.get(authorid, auth=(username, password)) # send get request to node to retrieve external author info
      author_data = response.json()

  else: # if the author of the post is saved on our server
      author = Author.objects.filter(id = authorid)
      author_data = author.values()[0]

  if request.method == 'GET': # Deal with this later to make it work with foreign authors
    '''Get a single post by an author'''

    author = [Author.objects.get(id=authorid)]
    if not Post.objects.filter(id=postid).exists():
        return HttpResponse(status=404)
    else:
      post = [Post.objects.get(id=postid)]
      post_data = serializers.serialize('json', post)
      author_data = serializers.serialize('json', author, fields=["id", "profileImage", "displayName", "github", "displayName"])

      results = '{"post": ', post_data, ', "author": ', author_data, '}'
      return HttpResponse(results, content_type='application/json')


@api_view(['POST'])
def new_post(request):
    if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)

    data ={}
    if request.method == 'POST':
        form = PostView(request.POST)
        if form.is_valid():
          post = form.save(commit=False)
          
          post.type = "post"
          post.title = form.cleaned_data["title"]
          post.author = user

          post.description = form.cleaned_data["description"]
          post.contentType = form.cleaned_data["contentType"]
          post.content = form.cleaned_data["content"]

          post.published = make_aware(datetime.datetime.now())
          post.visibility = form.cleaned_data["visibility"]
          
          # images
          form.save(commit = True)
          data['success'] = True
          data["id"] = post.id
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

def get_author_posts(request, authorid):
  '''Get all posts by an author'''
  author = [Author.objects.get(id=authorid)]
  
  posts = Post.objects.filter(author=author[0]).order_by('-published')
  data = serializers.serialize('json', posts)
  # author_data = serializers.serialize('json', author, fields=["type", "id", "host", "displayName", "url", "github", "profileImage"])
  author_data = serializers.serialize('json', author, fields=["id", "profileImage", "displayName", "github", "displayName"])

  results = '{"posts": ', data, ', "authors": ', author_data, '}'
  return HttpResponse(results, content_type='application/json')


def get_post_comments(request, authorid, postid):
    '''Get all comments on a post'''
    post = Post.objects.get(pk=postid)
    comments = Comment.objects.filter(postid=post)

    merged_data = []
    for comment in comments:
        author = Author.objects.get(pk=comment.author.id)
        author_data = {
            "username": author.username,
            "type": author.type,
            "id": str(author.id),
            "url": author.url,
            "host": author.host,
            "displayName": author.displayName,
            "github": author.github,
            "profileImage": author.profileImage
        }
        comment_data = {
            "author": author_data,
            "comment": comment.comment,
            "contentType": comment.contenttype,
            "published": comment.publishdate.isoformat(),
            "id": str(comment.id)
        }
        merged_data.append(comment_data)

    data = json.dumps(merged_data, indent=4)

    return HttpResponse(data, content_type='application/json')

def get_post_comment(request, authorid, postid, commentid):
    '''Get a single comment on a post'''
    comment = Comment.objects.get(id=commentid)

    merged_data = []
    author = Author.objects.get(pk=comment.author.id)
    author_data = {
        "type": author.type,
        "id": str(author.id),
        "url": author.url,
        "host": author.host,
        "displayName": author.displayName,
        "username": author.username,
        "github": author.github,
        "profileImage": author.profileImage
    }
    comment_data = {
        "author": author_data,
        "comment": comment.comment,
        "contentType": comment.contenttype,
        "published": comment.publishdate.isoformat(),
        "id": str(comment.id)
    }
    merged_data.append(comment_data)

    data = json.dumps(merged_data, indent=4)

    return HttpResponse(data, content_type='application/json')

def like_post(request, authorid, postid):
  '''Like or unlike a post'''
  post = Post.objects.get(pk=postid)
  data = {}
 

  if not LikePost.objects.filter(author = request.user, post = post).exists():
      LikePost.objects.create(author = request.user, post = post)
      post.likecount = F('likecount') + 1
      data["already_liked"] = False
  else:
      LikePost.objects.get(author=request.user, post=post).delete()
      post.likecount = F('likecount') - 1
      data["already_liked"] = True
  post.save()
  return JsonResponse(data = data)

def like_comment(request, authorid, postid, commentid):
  '''Like or unlike a post'''
  comment = Comment.objects.get(pk=commentid)
 
  if not LikeComment.objects.filter(author = request.user, comment = comment).exists():
      LikeComment.objects.create(author = request.user, comment = comment)
      comment.likecount = F('likecount') + 1

  else:
      LikeComment.objects.get(author=request.user, comment=comment).delete()
      comment.likecount = F('likecount') - 1

  comment.save()
  return HttpResponse("Success")

def make_comment(request):
    data ={}
    if request.method == 'POST':
        form = CommentView(request.POST)
        print(form, form.errors)
        if form.is_valid():  
            comment = form.save(commit=False)
            comment.comment = form.cleaned_data["comment"]
            comment.author = request.user
            naive_datetime = datetime.datetime.now()
            comment.publishdate = make_aware(naive_datetime)

            postid = form.cleaned_data.get("postid")
            post = Post.objects.get(pk=postid.id)
            comment.post = post
            comment.visibility = post.visibility
            post.count = F('count') + 1
            post.save()

            form.save(commit = True)
            data['success'] = True  
            comment.save()
            return JsonResponse(data) 
        else:
            data['success'] = False  
            return JsonResponse(data) 

    rend = CommentView().get(request)
    return rend

def delete_post(request):
  '''Delete a post'''
  data = {}

  data = json.loads(request.body)
  postid = data.get('postid')
  post = Post.objects.get(pk=postid)

  if request.user == post.author:
    post.delete()
    data['success'] = True
    return JsonResponse(data)
  
  else:
    data['success'] = False
    return JsonResponse(data)

def delete_comment(request):
  '''Delete a comment'''
  data = {}

  data = json.loads(request.body)
  commentid = data.get('id')
  comment = Comment.objects.filter(id=commentid)

  if request.user == comment.author:
    comment.delete()
    data['success'] = True
    return JsonResponse(data) 
  
  else:
    data['success'] = False
    return JsonResponse(data)
  
def edit_post(request):
  '''Edit a post'''
  data = {}
  postid = request.POST.get('postid')

  post = get_object_or_404(Post, pk=postid)
  if request.method == 'POST':
      post.title = request.POST.get('title')
      post.description = request.POST.get('description')
      post.content = request.POST.get('content')
      post.visibility = request.POST.get('visibility')
      post.contentType = request.POST.get('contentType')
      post.save()

  data['success'] = True

  return JsonResponse(data)

def share_post(request, authorid, postid):
  '''Share a post'''
  data = {}
  
  post = Post.objects.get(pk=postid)
  postAuthor = Author.objects.get(id=authorid)

  sharingAuthor = request.user

  if request.method == 'POST':
      if sharingAuthor == postAuthor:
        print("horrible sharing failure")
        data['success'] = False
        data['message'] = "Sharing own post"

      elif not Share.objects.filter(author = request.user, post = post).exists() and post.visibility == "PUBLIC":
        print("great sharing success")
        Share.objects.create(author = request.user, post = post)
        post.sharecount = F('sharecount') + 1
        post.save()
        data['success'] = True

      elif not Share.objects.filter(author = request.user, post = post).exists() and post.visibility != "PUBLIC":
        print("horrible sharing failure")
        data['success'] = False
        data['message'] = "Post not shareable"

      elif Share.objects.filter(author = request.user, post = post).exists():
        print("horrible sharing failure")
        data['success'] = False
        data['message'] = "Already shared"

  return JsonResponse(data)

def frontend_explorer(request, **kwargs):
  return render(request, "index.html")

def get_post_likes(request, authorid, postid):
    '''Get all likes for a post'''

    likes = LikePost.objects.filter(pk=postid)

    merged_data = []
    for like in likes:
        author = Author.objects.get(pk=like.author.id)
        author_data = {
            "type": "author",
            "id": str(author.id),
            "url": author.url,
            "host": author.host,
            "displayName": author.displayName,
            "github": author.github,
            "profileImage": author.profileImage
        }
        like_data = {
            "post": like.post.id,
            "author": author_data,
        }
        merged_data.append(like_data)

    data = json.dumps(merged_data, indent=4)

    return HttpResponse(data, content_type='application/json')

def get_author_liked(request, authorid):
    '''Get all likes from an author'''

    author = Author.objects.get(pk=authorid)
    merged_data = []

    likes = LikePost.objects.filter(author=author)

    for like in likes:
        author = Author.objects.get(pk=like.author.id)
        author_data = {
            "type": "author",
            "id": str(author.id),
            "url": author.url,
            "host": author.host,
            "displayName": author.displayName,
            "github": author.github,
            "profileImage": author.profileImage
        }
        like_data = {
            "post": str(like.post.id),
            "author": author_data,
        }
        merged_data.append(like_data)

    likes = LikeComment.objects.filter(author=author)

    for like in likes:
        author = Author.objects.get(pk=like.author.id)
        author_data = {
            "type": "author",
            "id": str(author.id),
            "url": author.url,
            "host": author.host,
            "displayName": author.displayName,
            "github": author.github,
            "profileImage": author.profileImage
        }
        like_data = {
            "comment": str(like.comment.id),
            "author": author_data,
        }
        merged_data.append(like_data)

    data = json.dumps(merged_data, indent=4)

    return HttpResponse(data, content_type='application/json')