# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from .models import Post, Comment, Share
from authentication.models import Author, Node, Following
from django.http import JsonResponse
from django import forms
import datetime
from django.db.models import F
from rest_framework.decorators import api_view
from django.utils.timezone import make_aware
import json
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from authentication.getuser import getUser

from itertools import chain
from operator import attrgetter
import urllib.request
from urllib.parse import unquote
import base64
from posts.serializers import PostSerializer, CommentSerializer
from django.core import serializers as django_serializers
from authentication.models import *
from authentication.serializer import *
from authentication.checkbasic import my_authenticate

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class PostView(forms.ModelForm):
    template_name = "post/post.html"

    def get(self, request):
        return render(request, "index.html")

    class Meta:
        model = Post
        # fields = ("type", "title", "id", "source", "origin", "description", "contentType", "content", "count", "comments", "published", "visibility")
        fields = ("title", "visibility", "description",
                  "contentType", "content")


class CommentView(forms.ModelForm):
    template_name = "comment/comment.html"

    def get(self, request):
        return render(request, "index.html")

    class Meta:
        model = Comment
        fields = ("comment", "post")


@api_view(['GET', 'DELETE', 'PUT'])
def handle_author_post(request, authorid, postid):
    ''' GET [local, remote] get the public post whose id is POST_ID
        DELETE [local] remove the post whose id is POST_ID
        PUT [local] update a post where its id is POST_ID
    '''

    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if Author.objects.filter(id=authorid).exists():
        author = Author.objects.get(id=authorid)
    else:
        return JsonResponse({"message": "Author not found", "success": False}, status=404)

    # LOCAL + REMOTE
    if request.method == 'GET':
        if Post.objects.filter(id=postid, author=author).exists():
            post = Post.objects.get(id=postid)
            post = PostSerializer(post, context={"request": request}).data
        else:
            return JsonResponse({"message": "Post not found", "success": False}, status=404)
        return JsonResponse(post, status=200)

    # LOCAL
    if request.method == 'DELETE':
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local users only"}, status=401)

        if Post.objects.filter(id=postid, author=author).exists():
            post = Post.objects.get(id=postid)
            if user == post.author and user.is_authenticated:
                post.delete()
                return JsonResponse({"message": "Post deleted", "success": True}, status=200)
            else:
                return JsonResponse({"message": "Unauthorized", "success": False}, status=401)
        else:
            return JsonResponse({"message": "Post not found", "success": False}, status=404)

    # LOCAL
    if request.method == 'PUT':
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local users only"}, status=401)

        if Post.objects.filter(id=postid, author=author).exists():
            post = Post.objects.get(id=postid)
            if user == post.author and user.is_authenticated:
                post.title = request.POST.get('title')
                post.description = request.POST.get('description')
                post.content = request.POST.get('content')
                post.contentType = request.POST.get('contentType')
                post.save()
                return JsonResponse({"message": "Post edited successfully", "success": True}, status=200)
            else:
                return JsonResponse({"message": "Unauthorized", "success": False}, status=401)
        else:
            return JsonResponse({"message": "Post not found", "success": False}, status=404)


def utility_get_posts(author_id, mode):
    '''Get all visible posts for an author'''
    items = []
    
@api_view(['POST'])
def new_local_post(request):
    ''' LOCAL
        POST /new_local_post/: This function is used locally only to create a new post. This endpoint is posted to by our frontend form. The addition of external posts to our db is handled by new_external_post function'''
    
    if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)

    if request.method == 'POST': # Create new post based on form data submitted on our frontend
        
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

          print("Post visibility:" , post.visibility)
          post.url = user.url + '/posts/' + str(post.id)
          
          form.save(commit = True)
          data ={}
          data['success'] = True
          data["id"] = post.id
          post.save()

          post_data = {
             
             "type": "post",
             "title": post.title,
             "id": post.id,
             "source": post.source,
             "origin": post.origin,
             "description": post.description,
             "contentType": post.contentType,
             "content": post.content,
             "author": {
                "type": "author",
                "id": user.id,
                "host": user.host,
                "displayName": user.displayName,
                "url": user.url,
                "github": user.github,
                "profileImage": user.profileImage
             },
             "count":0,
             "comments": None,
             "published": post.published,
             "visibility": "PUBLIC"

          }

          #-- Send post to relevant author's inboxes-- (I think we only need to send them to external authors?)

          if post.visibility == "PUBLIC":

            following = Following.objects.filter(followingid=user.id) # Users who will receive this post in their inbox
            
            for following_user in following:
              following_user = Author.objects.get(id=following_user.authorid)
              url = following_user.url
              host = following_user.host   # get the host from the id

              if Node.objects.filter(baseUrl = host).exists():
                node = Node.objects.get(baseUrl = host)
                username = node["theirUsername"]
                password = node["theirPassword"]
                requests.post(url + '/inbox/', post_data, auth=(username,password)) # Send to external author

              else:
                 requests.post(url + '/inbox/', post_data) # Send to author on our server (I don't think this is necessary but the spec is a bit unclear)
      
          # Send this post to the inboxes of authors who are friends with the posting author
          elif post.visibility == "FRIENDS":
             following = Following.objects.filter(followingid=user.id, areFriends=True) # Users who will receive this post in their inbox

             for following_user in following:
              following_user = Author.objects.get(id=following_user.authorid)
              url = following_user.url
              host = following_user.host  # get the host from the id


              if Node.objects.filter(baseUrl = host).exists():
                node = Node.objects.get(baseUrl = host)
                username = node["theirUsername"]
                password = node["theirPassword"]
                requests.post(url + '/inbox/', data,  auth=(username,password)) # Send to external author

              else:
                 requests.post(url + '/inbox/', data)  # Send to author on our server (I don't think this is necessary but the spec is unclear)

    author_object = Author.objects.get(id=author_id)
    print("MODE", mode)
    # Author
    if mode == "author":
        # All of my post
        items = chain(items, Post.objects.filter(
            author=author_object).order_by('-published'))

    # Friend of author, author_object now is a friend, not the user
    else:
        if mode == "friend":
            # Get their public posts
            items = chain(items, Post.objects.filter(
                author=author_object, visibility="FRIENDS").order_by('-published'))

        items = chain(items, Post.objects.filter(
            author=author_object, visibility="PUBLIC").order_by('-published'))

    sorted_items = sorted(items, key=attrgetter('published'), reverse=True)
    return sorted_items


@api_view(['GET'])
def get_all_posts(request):
    "This function retrieves all posts to display on the user's stream. Includes all public posts and any friends only posts or posts from followed users"

    user, session = getUser(request)
    session.save()
    if not user:
        return JsonResponse({"message": "User session error"})

    all_visible_posts = utility_get_posts(user.id, "author")

    authors = [Author.objects.get(id=(post.author.id))
               for post in all_visible_posts]
    author_data = django_serializers.serialize('json', authors, fields=[
        "id", "profileImage", "displayName", "github", "displayName"])
    stream_posts = django_serializers.serialize('json', all_visible_posts)

    results = '{"posts": ', stream_posts, ', "authors": ', author_data, '}'

    return HttpResponse(results, content_type='application/json')


def api_get_comments(request, authorid, postid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    # LOCAL + REMOTE
    if request.method == 'GET':
        if not Author.objects.filter(id=authorid).exists():
            return JsonResponse({"message": "Author not found", "success": False}, status=404)
        if not Post.objects.filter(id=postid).exists():
            return JsonResponse({"message": "Post not found", "success": False}, status=404)

        post = Post.objects.get(pk=postid)
        comments = Comment.objects.filter(post=post).order_by('-published')

        # Pagination
        page = request.GET.get('page')
        size = request.GET.get('size')
        if page and size:
            page = int(page)
            size = int(size)
            start_index = size * (page - 1)
            end_index = size * page

            if end_index > len(comments):
                end_index = len(comments)
            if start_index < 0:
                start_index = 0

            if start_index > len(comments) or end_index < 0:
                comments = []
            else:
                comments = comments[start_index: end_index]

        comment_serializer = CommentSerializer(
            instance=comments, context={"request": request}, many=True
        )
        result = {
            "type": "comments",
            "page": page,
            "size": size,
            "post": post.id,
            "id": post.comments,
            "comments": comment_serializer.data
        }
        return JsonResponse(result, status=200, safe=False)

    # LOCAL
    elif request.method == 'POST':
        if not isinstance(user, Author):
            return JsonResponse({"message": "Local users only"}, status=401)

        if user and user.is_authenticated:
            data = json.loads(request.body)

            naive_datetime = datetime.datetime.now()

def get_author_posts(request, authorid):
  '''Get all posts by an author'''
  author = [Author.objects.get(id=authorid)]
  page = request.GET.get('page', 1)
  size = request.GET.get('size', 10)
  
  posts = Post.objects.filter(author=author[0]).order_by('-published')
  paginator = Paginator(posts, size)
  try:
    posts_page = paginator.page(page)
  except PageNotAnInteger:
    posts_page = paginator.page(1)
  except EmptyPage:
    posts_page = paginator.page(paginator.num_pages)

  data = serializers.serialize('json', posts_page)
  # author_data = serializers.serialize('json', author, fields=["type", "id", "host", "displayName", "url", "github", "profileImage"])
  author_data = serializers.serialize('json', author, fields=["id", "profileImage", "displayName", "github", "displayName"])

            post = Post.objects.get(id=postid)
            post.count = F('count') + 1

            comment = Comment.objects.create(comment=data["comment"], author=user, post=post, published=make_aware(
                naive_datetime), contentType="text/plain", visibility=post.visibility)

            post.save()
            comment.save()

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

            comment_obj = CommentSerializer(
                comment, context={"request": request}).data
            return JsonResponse({"message": "Comment created", "success": True, "comment": comment_obj}, status=201)
        else:
            return JsonResponse({"message": "Unauthorized", "success": False}, status=401)


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
        "published": comment.published.isoformat(),
        "id": str(comment.id),
        "likecount": comment.likecount
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
  action_performed = "liked"
 
  if not LikeComment.objects.filter(author = request.user, comment = comment).exists():
      LikeComment.objects.create(author = request.user, comment = comment)
      comment.likecount = F('likecount') + 1
      comment.save()

  else:
      LikeComment.objects.get(author=request.user, comment=comment).delete()
      comment.likecount = F('likecount') - 1
      action_performed = "unliked"
      comment.save()

  comment.refresh_from_db()
  
  return JsonResponse({"success": True, "action": action_performed, "likecount": comment.likecount})


def make_comment(request):
    data = {}
    if request.method == 'POST':
        form = CommentView(request.POST)
        print(form, form.errors)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment = form.cleaned_data["comment"]
            comment.author = request.user
            naive_datetime = datetime.datetime.now()
            comment.published = make_aware(naive_datetime)

            post_form = form.cleaned_data.get("postid")
            post = Post.objects.get(pk=post_form.id)
            comment.post = post
            comment.visibility = post.visibility
            post.count = F('count') + 1
            post.save()

            form.save(commit=True)
            data['success'] = True
            comment.save()
            return JsonResponse(data)
        else:
            data['success'] = False
            return JsonResponse(data)

    rend = CommentView().get(request)
    return rend


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


def api_share_post(request, authorid, postid):
    '''Share a post'''
    if request.session.session_key is not None:
        session = Session.objects.get(
            session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            if Author.objects.filter(id=uid).exists():
                user = Author.objects.get(id=uid)

    post = Post.objects.get(pk=postid)
    post_json = PostSerializer(post, context={"request": request}).data
    if request.method == 'POST':
        if not Post.objects.filter(author=user, origin=post.origin).exists():
            shared_post = Post.objects.create(
                # Unchanged fierlds
                title=post.title,
                description=post.description,
                contentType=post.contentType,
                content=post.content,
                visibility=post.visibility,
                origin=post.origin,

                # Changed fields
                author=user,
                published=make_aware(datetime.datetime.now()),
                source=post_json["id"],
                likecount=0,
                sharecount=0,
                count=0,
            )
            return JsonResponse({"message": "Post shared", "success": True, "object": PostSerializer(instance=shared_post, context={"request": request}).data}, status=201)

        return JsonResponse({"message": "Post already shared", "success": False}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def frontend_explorer(request, **kwargs):
    return render(request, "index.html")


def api_posts(request, authorid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)

    # LOCAL + REMOTE
    if request.method == 'GET':
        # sort posts by authentication as author, friend of author, or public
        if user and str(user.id) == str(authorid) and isinstance(user, Author):
            posts = utility_get_posts(authorid, "author")
        elif user and user.id != authorid and isinstance(user, Author):
            author_object = Author.objects.get(id=authorid)
            author_json = AuthorSerializer(
                instance=author_object, context={"request": request}
            ).data
            user_json = AuthorSerializer(
                instance=user, context={"request": request}
            ).data
            if Follower.objects.filter(author=user, follower_author=author_json).exists() and Follower.objects.filter(author=author_object, follower_author=user_json).exists():
                posts = utility_get_posts(authorid, "friend")
            else:
                posts = utility_get_posts(authorid, "public")
        else:
            posts = utility_get_posts(authorid, "public")

        # params
        page = request.GET.get('page')
        size = request.GET.get('size')

        if page and size:
            page = int(page)
            size = int(size)

            start_index = size * (page - 1)
            end_index = size * page

            if end_index > len(posts):
                end_index = len(posts)
            if start_index < 0:
                start_index = 0

            if start_index > len(posts) or end_index < 0:
                posts = []
            else:
                posts = posts[(page - 1) * size: page * size]

        post_serializer = PostSerializer(
            posts, many=True, context={"request": request}
        )
        return JsonResponse({
            "type": "posts",
            "items": post_serializer.data
        }, status=200)

    # LOCAL
    if request.method == 'POST':
        if not isinstance(user, Author) or str(user.id) != str(authorid):
            return JsonResponse({"message": "Local users only"}, status=401)

        if request.session.session_key is not None:
            session = Session.objects.get(
                session_key=request.session.session_key)
            if session:
                session_data = session.get_decoded()
                uid = session_data.get('_auth_user_id')
                user = Author.objects.get(id=uid)

            if user and str(user.id) == str(authorid) and user.is_authenticated:
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
                    post.url = f"{user.host}espresso-api/authors/{user.id}/posts/{str(post.id)}"
                    post.comments = f"{user.url}posts/{str(post.id)}/comments"

                    post.origin = f"{user.host}espresso-api/authors/{user.id}/posts/{str(post.id)}"
                    post.source = f"{user.host}espresso-api/authors/{user.id}/posts/{str(post.id)}"

                    form.save(commit=True)
                    post.save()
                    return JsonResponse({"message": "Post created", "success": True, "postid": post.id, "object": PostSerializer(instance=post, context={"request": request}).data}, status=201)
                else:
                    return JsonResponse({"message": "Invalid form", "success": False}, status=400)
            else:
                return JsonResponse({"message": "Unauthorized", "success": False}, status=401)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def get_author_posts(request, authorid):
    if Author.objects.filter(id=authorid).exists():
        author = Author.objects.get(id=authorid)
        posts = Post.objects.filter(author=author).order_by('-published')

        result = []
        for post in posts:
            result.append({
                "type": "post",
                "title": post.title,
                "id": post.id,
                "source": post.source,
                "origin": post.origin,
                "description": post.description,
                "contentType": post.contentType,
                "content": post.content,
                "author": {
                    "type": "author",
                    "id": post.author.id,
                    "host": post.author.host,
                    "displayName": post.author.displayName,
                    "url": post.author.url,
                    "github": post.author.github,
                    "profileImage": post.author.profileImage
                },
                "count": post.count,
                "comments": post.comments,
                "published": post.published,
                "visibility": post.visibility,
                "likecount": post.likecount,
                "sharecount": post.sharecount,
            })
        return JsonResponse(result, status=200, safe=False)
    return HttpResponse(status=404)


def api_get_image(request, authorid, postid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)
    if not Post.objects.filter(id=postid).exists():
        return JsonResponse({"message": "Post not found", "success": False}, status=404)

    # LOCAL + REMOTE
    if request.method == 'GET':
        post = Post.objects.get(
            id=postid, author=Author.objects.get(id=authorid))
        if "image" in post.contentType.lower():
            base64_string = post.content
            no_prefix = base64_string.split(",")[1]
            image_binary = base64.b64decode(no_prefix)
            return HttpResponse(image_binary, content_type=post.contentType)
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotAllowed()


def api_get_feed(request):
    if request.method == 'GET':
        user = None
        if request.session.session_key is not None:
            session = Session.objects.get(
                session_key=request.session.session_key)
            if session:
                session_data = session.get_decoded()
                uid = session_data.get('_auth_user_id')
                if Author.objects.filter(id=uid).exists():
                    user = Author.objects.get(id=uid)

        if not user:
            return JsonResponse({"message": "Unauthorized", "success": False}, status=401)

        all_posts = []

        # Public posts
        public_posts = Post.objects.filter(
            visibility="PUBLIC").order_by('-published')

        # Unlisted posts + Friends posts from current user
        unlisted_posts = Post.objects.filter(
            visibility="UNLISTED", author=user).order_by('-published')
        friend_posts = Post.objects.filter(
            author=user, visibility="FRIENDS").order_by('-published')

        all_posts = chain(all_posts, public_posts,
                          unlisted_posts, friend_posts)

        # Friends posts from friends
        friends = Follower.objects.filter(author=user)

        for friend in friends:
            raw_id = friend.follower_author["id"].split("/")[-1]
            friend_object = Author.objects.get(
                id=raw_id)
            other_posts = Post.objects.filter(
                author=friend_object, visibility="FRIENDS").order_by('-published')
            all_posts = chain(all_posts, other_posts)

        sorted_posts = sorted(
            all_posts, key=attrgetter('published'), reverse=True)

        # Return the posts
        post_serializer = PostSerializer(
            sorted_posts, many=True, context={"request": request}
        )

        return JsonResponse({
            "type": "posts",
            "items": post_serializer.data
        }, status=200)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
