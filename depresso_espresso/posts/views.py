import base64
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from authentication.checkbasic import my_authenticate
from posts.models import *
from posts.serializers import *
from authentication.models import Author, Following, Node
from inbox.models import NotificationItem
from django.db.models import Q
from itertools import chain
from requests.auth import HTTPBasicAuth
import requests
from inbox.views import create_notification_item
from inbox.models import Notification, NotificationItem
from drf_yasg.utils import swagger_auto_schema
from utils import Pagination
from urllib.parse import urlparse


def get_posts(current_user, author_object):
    '''
    This function returns the posts of an author based on the current user
    '''
    if current_user is None:
        return []
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


@swagger_auto_schema(tags=['Posts'], methods=["GET", "POST"])
@api_view(['GET', 'POST'])
def api_posts(request, author_id):

    user = my_authenticate(request)

    if request.method == 'GET':
        if not Author.objects.filter(id=author_id).exists():
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        author = Author.objects.get(id=author_id)
        posts = get_posts(user, author)

        paginator = Pagination("posts")
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(
            page, context={"request": request}, many=True)
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
                new_shared_post = serializer.save(origin=old_id)

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
                        requests.post(f"{author_url.rstrip('/')}/inbox",
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
                    node = Node.objects.filter(
                        baseUrl=author_host.rstrip("/") + "/")
                    if node:
                        node = node.first()
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        requests.post(f"{author_url.rstrip('/')}/inbox",
                                      json=returned_data, auth=auth)
                    else:
                        notification_object = Notification.objects.get_or_create(
                            author=following_author)[0]
                        create_notification_item(
                            notification_object, new_post, "post")

            elif new_post.visibility == "FRIENDS":

                friends_following_objects = following_objects.filter(
                    areFriends=True)
                for following_object in friends_following_objects:
                    following_author = following_object.following_author
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.filter(baseUrl=author_host)
                    if node:
                        node = node.first()
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        requests.post(f"{author_url.rstrip('/')}/inbox",
                                      json=returned_data, auth=auth)
                    else:
                        notification_object = Notification.objects.get_or_create(
                            author=following_author)[0]
                        create_notification_item(
                            notification_object, new_post, "post")

            return JsonResponse(
                {
                    "success": True,
                    "object": returned_data
                }, status=201)
        else:
            return JsonResponse(serializer.errors, status=501)


def api_feed(request):
    user = my_authenticate(request)
    if request.method == 'GET':

        feed = []

        public_posts = Post.objects.filter(
            visibility="PUBLIC")
        for public_post in public_posts:
            if public_post.author.isExternalAuthor == True and not Following.objects.filter(
                    author=public_post.author, following_author=user).exists():
                public_posts = public_posts.exclude(id=public_post.id)

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
            friends_only_posts = Post.objects.filter(
                Q(author=following_author), Q(visibility="FRIENDS"))
            feed = chain(feed, PostSerializer(
                instance=friends_only_posts, many=True, context={"request": request}).data)

        feed = list(
            chain(feed, public_posts, friends_unlisted_posts))

        feed = sorted(feed, key=lambda x: x["published"], reverse=True)
        return JsonResponse({"type": "posts", "items": feed}, safe=False)
    else:
        return JsonResponse({"error": "Invalid request"}, status=405)


@swagger_auto_schema(tags=['Posts'], methods=["GET", "PUT", "DELETE"])
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
            object_id=post.id)

        for notification_object in notification_objects:
            notification_object.delete()
        post.delete()

        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"error": "Invalid request"}, status=405)


@swagger_auto_schema(tags=['Comments'], methods=["GET", "POST"])
@api_view(['GET', 'POST'])
def api_comments(request, author_id, post_id):
    user = my_authenticate(request)
    if request.method == 'GET':
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)

        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-published')

        paginator = Pagination("comments")
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(
            page, context={"request": request}, many=True)

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

                # if this post has been shared on external servers, update their comments too

                # get all followers of the post author
                following_objects = Following.objects.filter(
                    author=user)
                
                print("Following obs:", following_objects)
                for following_object in following_objects:
                    following_author = following_object.following_author
                    author_url = following_author.url
                    author_host = following_author.host
                    node = Node.objects.filter(baseUrl=author_host)
                    # if they are external authors, send comment ob to them
                    if node:
                        node = node.first()
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        
                        print("COMMENT JSON:", returned_data)
                        print("author url:", author_url.rstrip('/'))
                        requests.post(f"{author_url.rstrip('/')}/inbox",
                                      json=returned_data, auth=auth)

            else:
                nodes = Node.objects.all()
                for node in nodes:
                    if node.baseUrl == post_owner_host:
                        auth = HTTPBasicAuth(
                            node.ourUsername, node.ourPassword)
                        
                        print("COMMENT JSON:", returned_data)
                        print("author url:", author_url.rstrip('/'))
                        requests.post(f"{post_owner_url}/inbox",
                                      json=returned_data, auth=auth)
                        

            return JsonResponse(
                returned_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=501)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


@swagger_auto_schema(tags=['Posts'], methods=["GET"])
@api_view(['GET'])
def api_get_image(request, author_id, post_id):
    user = my_authenticate(request)

    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({"message": "Author not found", "success": False}, status=404)
    if not Post.objects.filter(id=post_id).exists():
        return JsonResponse({"message": "Post not found", "success": False}, status=404)

    if request.method == 'GET':
        post = Post.objects.get(
            id=post_id, author=Author.objects.get(id=author_id))
        if "image" in post.contenttype.lower():
            base64_string = post.content
            no_prefix = base64_string.split(",")[1]
            image_binary = base64.b64decode(no_prefix)
            return HttpResponse(image_binary, content_type=post.contenttype)
        else:
            return JsonResponse({"message": "Post is not an image", "success": True}, status=404)
    else:
        return JsonResponse({"message": "Method not Allowed", "success": False}, status=405)


@swagger_auto_schema(tags=['Posts'], methods=["GET"])
@api_view(['GET'])
def api_post_like(request, author_id, post_id):
    if request.method == 'GET':
        user = my_authenticate(request)
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)

        post = Post.objects.get(id=post_id)
        post_like_list = LikePost.objects.filter(
            post=post)
        data = LikePostSerializer(instance=post_like_list, context={
            "request": request}, many=True).data
        return JsonResponse({"type": "Like", "items": data}, safe=False)
    else:
        return JsonResponse({"error": "Method not Allowed", "success": False}, status=405)


@swagger_auto_schema(tags=['Comments'], methods=["GET"])
@api_view(['GET'])
def api_comment_like(request, author_id, post_id, comment_id):
    if request.method == 'GET':
        user = my_authenticate(request)
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({"error": "Comment not found", "success": False}, status=404)

        comment = Comment.objects.get(id=comment_id)
        comment_like_list = LikeComment.objects.filter(
            comment=comment)
        data = LikeCommentSerializer(instance=comment_like_list, context={
            "request": request}, many=True).data
        return JsonResponse({"type": "Like", "items": data}, safe=False)
    else:
        return JsonResponse({"error": "Method not Allowed", "success": False}, status=405)


@api_view(['POST'])
def api_likes(request, author_id, post_id):
    if (request.method == 'POST'):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"error": "Post not found", "success": False}, status=404)
        else:
            liked_post = Post.objects.get(id=post_id)
            post_author = liked_post.author

            like_author = request.data.get("author")
            if not Author.objects.filter(url=like_author.get("url")).exists():

                serializer = AuthorSerializer(
                    data=like_author, context={"request": request})
                if serializer.valid():
                    like_author = serializer.save()
                else:
                    return JsonResponse(serializer.errors, status=501)
            else:
                like_author = Author.objects.get(
                    url=like_author.get("url"))

            data = request.data
            data["post_id"] = Post.objects.get(id=post_id)
            serializer = LikePostSerializer(
                data=data, context={"request": request})

            if serializer.is_valid():
                new_like = LikePost.objects.create(
                    author=like_author, post=liked_post)

                returned_data = LikePostSerializer(
                    instance=new_like, context={"request": request}).data
                returned_data.pop("post", None)

                if not post_author.isExternalAuthor:
                    notification_object = Notification.objects.get_or_create(author=like_author)[
                        0]

                    like_object = new_like

                    create_notification_item(
                        notification_object, like_object, "like")

                    followers = Following.objects.filter(author=post_author)

                    for follower in followers:
                        if follower.following_author.isExternalAuthor:
                            node = Node.objects.get(
                                baseUrl=follower.following_author.host)
                            auth = HTTPBasicAuth(
                                node.ourUsername, node.ourPassword)
                            response = requests.post(f"{follower.following_author.url.rstrip('/')}/inbox",
                                                     json=returned_data, auth=auth)
                            print("Sent to ", follower.following_author.url)
                            print(response.status_code)

                else:
                    nodes = Node.objects.all()
                    for node in nodes:
                        if node.baseUrl == post_author.host:
                            auth = HTTPBasicAuth(
                                node.ourUsername, node.ourPassword)
                            response = requests.post(f"{post_author.url}/inbox",
                                                     json=returned_data, auth=auth, headers={"origin": request.META["HTTP_HOST"]})
                            print("Sent to ", post_author.url)
                            print(response.status_code)
                return JsonResponse(
                    returned_data, status=201)
            else:
                return JsonResponse(serializer.errors, status=501)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


# FRONTEND URLS

def node_auth_helper(url):
    for node in Node.objects.all():
        if node.baseUrl in url:
            auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
            return auth
    return None


@api_view(['POST', 'GET', 'PUT'])
def api_execute(request):
    url = request.data["url"]
    method = request.data["method"]
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    schema = urlparse(url)
    hostname = '{uri.scheme}://{uri.netloc}/'.format(uri=schema)

    if method == "GET":
        if (request.META["HTTP_HOST"] in hostname):  # Same host
            session = requests.Session()
            r = session.get(url, headers={"origin": request.META["HTTP_HOST"]})
            if r.status_code == 200:
                return JsonResponse(r.json(), status=200)
            else:
                return HttpResponse(r.text, status=r.status_code)
        else:
            auth = node_auth_helper(hostname)
            if not auth:
                return JsonResponse({"message": "Node not found"}, status=404)
            response = requests.get(url, auth=auth, headers={
                "origin": request.META["HTTP_HOST"]
            })

            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                try:
                    response_json = response.json()
                    return JsonResponse(response_json, status=response.status_code)
                except:
                    return HttpResponse(response.text, status=404)

    # POST external API
    elif method == "POST":
        obj = request.data["data"]
        if (request.META["HTTP_HOST"] in hostname):  # Same host
            session = requests.Session()
            r = session.post(url, json=obj, headers={
                "origin": request.META["HTTP_HOST"]})
            if r.status_code == 201:
                return JsonResponse(r.json(), status=201)
            return r
        else:
            auth = node_auth_helper(hostname)

            if not auth:
                return JsonResponse({"message": "Node not found"}, status=404)
            
            print(f'ORIGINAL sending {obj} to {url}')
            
            if obj.get('object') != None:
                author_url = obj['object']['url']
                if author_url[-1] == '/':
                    author_url = author_url.rstrip('/')

                obj['object']['id'] = author_url

            
            print(f'sending {obj} to {url}')
            response = requests.post(url, json=obj, auth=auth, headers={
                "origin": request.META["HTTP_HOST"]
            })

            print("\nRESPONSE:", response)
            print("\nRESPONSE text:", response.text)
            print("\nRESPONSE dict:", json.loads(response.text))

            if response.status_code == 201:
                return JsonResponse(response.json(), status=201)

    # PUT external API
    elif method == "PUT":
        obj = request.data["data"]
        if (request.META["HTTP_HOST"] in url):  # Same host
            session = requests.Session()

            r = session.put(url, json=obj, headers={
                "origin": request.META["HTTP_HOST"]})

            if r.status_code == 200 or r.status_code == 201:
                return JsonResponse(r.json(), safe=False, status=r.status_code)
        else:
            auth = node_auth_helper(url)
            if not auth:
                return JsonResponse({"message": "Node not found"}, status=404)

            response = requests.put(url, json=obj, auth=auth, headers={
                "origin": request.META["HTTP_HOST"]
            })
            if response.status_code == 200:
                return JsonResponse(response.json(), safe=False, status=200)

    return JsonResponse({"message": "If you see this message, it means something's wrong"}, status=404)
