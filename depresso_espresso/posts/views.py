from rest_framework.decorators import api_view
from django.http import JsonResponse
from authentication.checkbasic import my_authenticate
from posts.models import *
from posts.serializers import *
from authentication.models import Author, Following, Node
from django.db.models import Q
from itertools import chain
from requests.auth import HTTPBasicAuth
import requests


def get_posts(current_user, author_object):
    '''
    This function returns the posts of an author based on the current user
    '''
    if current_user.id == author_object.id:
        return Post.objects.filter(author=author_object).order_by('-published')
    else:
        following_object = Following.objects.filter(
            author=current_user, following_author=author_object)
        if following_object.exists() and following_object[0].areFriends:
            return Post.objects.filter(
                Q(author=author_object) & ~Q(visibility="UNLISTED")).order_by('-published')
        else:
            return Post.objects.filter(
                Q(author=author_object) & Q(visibility="PUBLIC")).order_by('-published')


@api_view(['GET', 'POST'])
def api_posts(request, author_id):

    user = my_authenticate(request)

    if request.method == 'GET':
        if not Author.objects.filter(id=author_id).exists():
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        author = Author.objects.get(id=author_id)
        posts = get_posts(user, author)
        serializer = PostSerializer(
            posts, context={"request": request}, many=True)
        return JsonResponse({"type": "posts", "items": serializer.data}, safe=False)

    elif request.method == 'POST':
        data = request.data
        serializer = PostSerializer(
            data=data, context={"request": request})

        if serializer.is_valid():
            new_post = serializer.save()

            returned_data = PostSerializer(instance=new_post, context={
                                           "request": request}).data

            following_objects = Following.objects.filter(
                author=user)

            if new_post.visibility == "PUBLIC":
                for following_object in following_objects:
                    following_author = following_object.following_author
                    print(following_author.displayName)
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.get(baseUrl=author_host)
                    auth = HTTPBasicAuth(
                        node.ourUsername, node.ourPassword)
                    requests.post(f"{author_url}/inbox",
                                  json=returned_data, auth=auth)

                    # print(response)

            elif new_post.visibility == "FRIENDS":

                friends_following_objects = following_objects.filter(
                    areFriends=True)

                for following_object in friends_following_objects:
                    following_author = following_object.following_author
                    print(following_author.displayName)
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.get(baseUrl=author_host)
                    auth = HTTPBasicAuth(
                        node.ourUsername, node.ourPassword)
                    requests.post(f"{author_url}/inbox",
                                  json=returned_data, auth=auth)

                    # print(response)

            return JsonResponse(
                {
                    "success": True,
                    "object": returned_data
                }, status=201)
        else:
            return JsonResponse(serializer.errors, status=501)


@api_view(['GET'])
def api_feed(request):
    user = my_authenticate(request)
    if request.method == 'GET':

        public_posts = Post.objects.filter(
            visibility="PUBLIC")

        friends_unlisted_posts = Post.objects.filter(
            Q(visibility="FRIENDS") | Q(visibility="UNLISTED"), Q(author=user))

        Following_objects = Following.objects.filter(
            author=user, areFriends=True)

        my_friend_posts = []

        for following in Following_objects:
            my_friend_posts = chain(my_friend_posts,
                                    Post.objects.filter(author=following.following_author, visibility="FRIENDS"))

        feed = list(
            chain(public_posts, friends_unlisted_posts, my_friend_posts))

        feed = sorted(feed, key=lambda x: x.published, reverse=True)

        serializer = PostSerializer(
            feed, many=True, context={"request": request})
        return JsonResponse({"type": "posts", "items": serializer.data}, safe=False)
    else:
        return JsonResponse({"error": "Invalid request"}, status=405)


@api_view(['GET', 'PUT', 'DELETE'])
def api_post(request, author_id, post_id):

    user = my_authenticate(request)

    if request.method == 'GET':
        if not Author.objects.filter(id=author_id).exists():
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        author = Author.objects.get(id=author_id)
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)

        post = Post.objects.get(id=post_id)

        serializer = PostSerializer(
            instance=post, context={"request": request})

        return JsonResponse(serializer.data, status=200)

    if request.method == 'PUT':
        if not Author.objects.filter(id=author_id).exists():
            return JsonResponse({"error": "Author not found", "success": False}, status=404)

        author = Author.objects.get(id=author_id)

        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)

        post = Post.objects.get(id=post_id)

        if post.author != author:
            return JsonResponse({"error": "You are not the author of this post", "success": False}, status=403)

        data = request.data

        serializer = PostSerializer(
            instance=post, data=data, context={"request": request})

        if serializer.is_valid():

            new_post = serializer.save()

            returned_data = PostSerializer(instance=new_post, context={
                                           "request": request}).data
            return JsonResponse(
                returned_data, status=200)
        else:
            return JsonResponse(serializer.errors, status=501)

    elif request.method == 'DELETE':
        if not Author.objects.filter(id=author_id).exists():
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        author = Author.objects.get(id=author_id)
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
        post = Post.objects.get(id=post_id)
        if post.author != author:
            return JsonResponse({"error": "You are not the author of this post", "success": False}, status=403)
        post.delete()
        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"error": "Invalid request"}, status=405)
