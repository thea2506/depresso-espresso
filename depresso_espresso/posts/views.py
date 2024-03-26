from rest_framework.decorators import api_view
from django.http import JsonResponse
from authentication.checkbasic import my_authenticate
from posts.models import *
from posts.serializers import *
from authentication.models import Author, Following, Node
from inbox.models import NotificationItem
from django.db.models import Q
from itertools import chain
from requests.auth import HTTPBasicAuth
import requests
from inbox.views import handle_comment, create_notification_item
from inbox.models import Notification, NotificationItem

from authors.views import get_author_object


def get_posts(current_user, author_object):
    '''
    This function returns the posts of an author based on the current user
    '''
    if current_user.id == author_object.id:
        return Post.objects.filter(author=author_object).order_by('-published')
    else:
        following_object = Following.objects.filter(
            author__url=current_user.url, following_author=author_object)
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

        if data.get("id") is not None:
            old_id = data.get("id")
            # Share
            shared_post = data
            shared_post.pop("id", None)
            shared_post["type"] = "share"

            shared_post["author"] = AuthorSerializer(
                instance=user, context={"request": request}).data

            shared_post["source"] = old_id

            serializer = PostSerializer(data=shared_post, context={
                                        "request": request})

            if serializer.is_valid():
                new_shared_post = serializer.save()

                returned_data = PostSerializer(instance=new_shared_post, context={
                                               "request": request}).data

                following_objects = Following.objects.filter(
                    author=user)

                for following_object in following_objects:
                    following_author = following_object.following_author
                    author_url = following_author.url
                    author_host = following_author.host

                    if following_author.isExternalAuthor:

                        node = Node.objects.get(baseUrl=author_host)
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        requests.post(f"{author_url}/inbox",
                                      json=returned_data, auth=auth)

                    else:
                        notification_object = Notification.objects.get_or_create(
                            author=following_author)[0]
                        create_notification_item(
                            notification_object, new_shared_post, "share")

                return JsonResponse(
                    returned_data, status=201)

            return JsonResponse(serializer.errors, status=405)

        else:
            data["type"] = "post"

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
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.filter(baseUrl=author_host)
                    if node:
                        node = node.first()
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        requests.post(f"{author_url}/inbox",
                                      json=returned_data, auth=auth)

            elif new_post.visibility == "FRIENDS":

                friends_following_objects = following_objects.filter(
                    areFriends=True)

                for following_object in friends_following_objects:
                    following_author = following_object.following_author
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.get(baseUrl=author_host)
                    auth = HTTPBasicAuth(
                        node.ourUsername, node.ourPassword)
                    requests.post(f"{author_url}/inbox",
                                  json=returned_data, auth=auth)

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

        feed = []

        public_posts = Post.objects.filter(
            visibility="PUBLIC")

        public_posts = PostSerializer(
            instance=public_posts, many=True, context={"request": request}).data

        friends_unlisted_posts = Post.objects.filter(
            Q(visibility="FRIENDS") | Q(visibility="UNLISTED"), Q(author=user))

        friends_unlisted_posts = PostSerializer(
            instance=friends_unlisted_posts, many=True, context={"request": request}).data

        following_objects = Following.objects.filter(
            author=user, areFriends=True)

        for following in following_objects:
            following_author = following.following_author
            if following_author.isExternalAuthor:
                author_url = following_author.url
                node = Node.objects.get(baseUrl=following_author.host)
                auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
                response = requests.get(
                    f"{author_url}/posts", auth=auth, headers={"origin": request.META["HTTP_HOST"]}, params=AuthorSerializer(instance=user, context={"request": request}).data)
                feed = chain(feed, response.json()["items"])
            else:
                my_friend_posts = Post.objects.filter(
                    author=following_author, visibility="FRIENDS")
                my_friend_posts = PostSerializer(
                    instance=my_friend_posts, many=True, context={"request": request}).data
                feed = chain(feed, my_friend_posts)

        feed = list(
            chain(feed, public_posts, friends_unlisted_posts))

        feed = sorted(feed, key=lambda x: x["published"], reverse=True)
        return JsonResponse({"type": "posts", "items": feed}, safe=False)
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

        notification_objects = NotificationItem.objects.filter(
            object_url=post.id)
        notification_objects.delete()
        post.delete()

        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"error": "Invalid request"}, status=405)


@api_view(['GET', 'POST'])
def api_comments(request, author_id, post_id):
    user = my_authenticate(request)
    if request.method == 'GET':
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-published')
        serializer = CommentSerializer(
            comments, context={"request": request}, many=True)
        return JsonResponse({"type": "comments", "items": serializer.data}, safe=False)

    elif request.method == 'POST':
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
        post = Post.objects.get(id=post_id)
        data = request.data
        data["post"] = post.id
        serializer = CommentSerializer(
            data=data, context={"request": request})
        if serializer.is_valid():

            new_comment = serializer.save()

            returned_data = CommentSerializer(
                instance=new_comment, context={"request": request}).data

            returned_data.pop("post", None)

            post_owner = post.author
            post_owner_url = post_owner.url

            post_owner_host = post_owner.host



            # Local Author
            if post_owner.isExternalAuthor == False:
                notification_object = Notification.objects.get_or_create(author=post_owner)[
                    0]

                comment_object = new_comment

                create_notification_item(
                    notification_object, comment_object, "comment")

            else:

                nodes = Node.objects.all()
                for node in nodes:
                    if node.baseUrl == post_owner_host:
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        print("sending comment...")
                        requests.post(f"{post_owner_url}/inbox",
                                      json=returned_data, auth=auth)

            return JsonResponse(
                returned_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=501)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


@api_view(['POST'])
def api_likes(request, author_id, post_id):
    if (request.method == 'POST'):
          if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
          else:
            liked_post = Post.objects.get(id=post_id)
            author = liked_post.author


            data = request.data
            data["post_id"]= Post.objects.get(id=post_id)
            print("data:", data)
            serializer = LikePostSerializer(
                data=data, context={"request": request})
            

            if serializer.is_valid():
                print("HEREEEEEEEEEEEEEEEE")
                new_like = LikePost.objects.create(author = author, post = liked_post)
                print("SLGFHSLFKHJSLFKJHL")

                returned_data = LikePostSerializer(
                instance=new_like, context={"request": request}).data
                returned_data.pop("post", None)

                if author.isExternalAuthor == False:
                    notification_object = Notification.objects.get_or_create(author=author)[
                        0]

                    like_object = new_like

                    create_notification_item(
                        notification_object, like_object, "like")



                if author.isExternalAuthor == True:
                    nodes = Node.objects.all()
                    for node in nodes:
                        if node.baseUrl == author.host:
                            auth = HTTPBasicAuth(
                                node.ourUsername, node.ourPassword)
                            print("sending like...")
                            requests.post(f"{author.url}/inbox",
                                        json=returned_data, auth=auth)
                            
                        
                return JsonResponse(
                    returned_data, status=201)
            else:
                return JsonResponse(serializer.errors, status=501)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)

                  
                  

              




@api_view(['POST'])
def api_likes(request, author_id, post_id):
    if (request.method == 'POST'):
          if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
          else:
            liked_post = Post.objects.get(id=post_id)
            author = liked_post.author


            data = request.data
            data["post_id"]= Post.objects.get(id=post_id)
            print("data:", data)
            serializer = LikePostSerializer(
                data=data, context={"request": request})
            

            if serializer.is_valid():
                print("HEREEEEEEEEEEEEEEEE")
                new_like = LikePost.objects.create(author = author, post = liked_post)
                print("SLGFHSLFKHJSLFKJHL")

                returned_data = LikePostSerializer(
                instance=new_like, context={"request": request}).data

                print(returned_data, "returned data:::")

                if author.isExternalAuthor == False:
                    notification_object = Notification.objects.get_or_create(author=author)[
                        0]

                    like_object = new_like

                    create_notification_item(
                        notification_object, like_object, "like")



                if author.isExternalAuthor == True:
                    nodes = Node.objects.all()
                    for node in nodes:
                        if node.baseUrl == author.host:
                            auth = HTTPBasicAuth(
                                node.ourUsername, node.ourPassword)
                            print("sending like...")
                            requests.post(f"{author.url}/inbox",
                                        json=returned_data, auth=auth)
                            
                        
                return JsonResponse(
                    returned_data, status=201)
            else:
                return JsonResponse(serializer.errors, status=501)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)

                  
                  

              



