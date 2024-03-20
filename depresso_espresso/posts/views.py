# Referece: https://stackoverflow.com/questions/22739701/django-save-modelform answer from Bibhas Debnath 2024-02-23
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from .models import Post, Comment, LikePost, LikeComment, Share
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

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    # Get the author (LOCAL or REMOTE)
    if Author.objects.filter(id=authorid).exists():
        author = Author.objects.get(id=authorid)
    else:
        response = urllib.request.urlopen(unquote(authorid))
        if response != 200:
            return JsonResponse({"message": "Foreign author not found", "success": False}, status=404)
        author = json.loads(response.read())

    if request.method == 'GET':
        # LOCAL POST
        if Post.objects.filter(id=postid, author=author).exists():
            post = Post.objects.get(id=postid)
            post = {
                "type": "post",
                "title": post.title,
                "id": f"{post.origin}/authors/{user.id}/posts/{post.id}",
                "source": post.source,
                "origin": post.origin,
                "description": post.description,
                "contentType": post.contentType,
                "content": post.content,
                "author": {
                    "type": "author",
                    "id": author.url,
                    "host": author.host,
                    "displayName": author.displayName,
                    "url": author.url,
                    "github": author.github,
                    "profileImage": author.profileImage
                },
                "count": post.count,
                "comments": f"{post.origin}/authors/{user.id}/posts/{post.id}/comments",
                "published": post.published,
                "visibility": post.visibility,
            }

        # REMOTE POST
        else:
            response = urllib.request.urlopen(f"{unquote(postid)}")
            if response != 200:
                return JsonResponse({"message": "Post not found", "success": False}, status=404)
            post = json.loads(response.read())
        return JsonResponse(post, status=200)

    if request.method == 'DELETE':
        if Post.objects.filter(id=postid, author=author).exists():
            post = Post.objects.get(id=postid)
            if user == post.author and user.is_authenticated:
                post.delete()
                return JsonResponse({"message": "Post deleted", "success": True}, status=200)
            else:
                return JsonResponse({"message": "Unauthorized", "success": False}, status=401)
        else:
            return JsonResponse({"message": "Post not found", "success": False}, status=404)

    if request.method == 'PUT':
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
    print("ST", items, sorted_items)
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
    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            if Author.objects.filter(id=uid).exists():
                user = Author.objects.get(id=uid)

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

    elif request.method == 'POST':
        if user and user.is_authenticated:
            data = json.loads(request.body)

            naive_datetime = datetime.datetime.now()

            post = Post.objects.get(id=postid)
            post.count = F('count') + 1

            comment = Comment.objects.create(comment=data["comment"], author=user, post=post, published=make_aware(
                naive_datetime), contentType="text/plain", visibility=post.visibility)

            post.save()
            comment.save()

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

    if not LikePost.objects.filter(author=request.user, post=post).exists():
        LikePost.objects.create(author=request.user, post=post)
        post.likecount = F('likecount') + 1
        data["already_liked"] = False
    else:
        LikePost.objects.get(author=request.user, post=post).delete()
        post.likecount = F('likecount') - 1
        data["already_liked"] = True
    post.save()
    return JsonResponse(data=data, status=200)


def like_comment(request, authorid, postid, commentid):
    '''Like or unlike a post'''
    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)
    if not Post.objects.filter(id=postid).exists():
        return JsonResponse({"message": "Post not found", "success": False}, status=404)
    if not Comment.objects.filter(id=commentid).exists():
        return JsonResponse({"message": "Comment not found", "success": False}, status=404)

    comment = Comment.objects.get(pk=commentid)
    data = {}
    if not LikeComment.objects.filter(author=request.user, comment=comment).exists():
        LikeComment.objects.create(author=request.user, comment=comment)
        comment.likecount = F('likecount') + 1
        data["already_liked"] = False
    else:
        LikeComment.objects.get(author=request.user, comment=comment).delete()
        comment.likecount = F('likecount') - 1
        data["already_liked"] = False

    comment.save()
    return JsonResponse(data, safe=False, status=200)


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

        elif not Share.objects.filter(author=request.user, post=post).exists() and post.visibility == "PUBLIC":
            print("great sharing success")
            Share.objects.create(author=request.user, post=post)
            post.sharecount = F('sharecount') + 1
            post.save()
            data['success'] = True

        elif not Share.objects.filter(author=request.user, post=post).exists() and post.visibility != "PUBLIC":
            print("horrible sharing failure")
            data['success'] = False
            data['message'] = "Post not shareable"

        elif Share.objects.filter(author=request.user, post=post).exists():
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


def api_posts(request, authorid):
    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)
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

        # sort posts by authentication as author, friend of author, or public
        if user and str(user.id) == str(authorid):
            posts = utility_get_posts(authorid, "author")
        elif user and user.id != authorid:
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

    if request.method == 'POST':
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
                    post.url = f"{user.url}/posts/{str(post.id)}"
                    post.comments = f"{user.url}/posts/{str(post.id)}/comments"

                    post.origin = f"{user.url}/posts/{str(post.id)}"
                    post.source = f"{user.url}/posts/{str(post.id)}"

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
    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)
    if not Post.objects.filter(id=postid).exists():
        return JsonResponse({"message": "Post not found", "success": False}, status=404)

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
