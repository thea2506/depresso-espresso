from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, Following, FollowRequest
from authentication.serializers import AuthorSerializer
from inbox.models import NotificationItem
from posts.models import LikePost, LikeComment
from posts.serializers import LikePostSerializer, LikeCommentSerializer
from authentication.models import Node
from django.contrib.contenttypes.models import ContentType
from depresso_espresso.constants import *
from requests.auth import HTTPBasicAuth
import requests
from urllib.parse import unquote
from urllib.parse import urlparse
from itertools import chain
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from utils import Pagination


def get_author_object(author_url):
    author_url = unquote(author_url)
    if "127.0.0.1" in author_url:
        normalized_author_url = author_url.replace("127.0.0.1", "localhost")
    elif "localhost" in author_url:
        normalized_author_url = author_url.replace("localhost", "127.0.0.1")
    else:
        normalized_author_url = author_url
    if not Author.objects.filter(url=author_url).exists() and not Author.objects.filter(
            url=normalized_author_url).exists() and not Author.objects.filter(url=author_url + "/").exists() and not Author.objects.filter(url=normalized_author_url + "/").exists():
        return None
    if Author.objects.filter(url=author_url).exists():
        return Author.objects.get(url=author_url)
    if Author.objects.filter(url=author_url + "/").exists():
        return Author.objects.get(url=author_url + "/")
    if Author.objects.filter(url=normalized_author_url).exists():
        return Author.objects.get(url=normalized_author_url)
    if Author.objects.filter(url=normalized_author_url + "/").exists():
        return Author.objects.get(url=normalized_author_url + "/")
    return None


@swagger_auto_schema(tags=['Authors'], methods=["GET"])
@api_view(['GET'])
def api_authors(request):
    if request.method == 'GET':
        authors = Author.objects.filter(
            Q(isExternalAuthor=False) & ~Q(url="") & ~Q(url=None))

        # Pagination
        paginator = Pagination("authors")
        page = paginator.paginate_queryset(authors, request)
        serializer = AuthorSerializer(
            page, context={'request': request},  many=True)

        return JsonResponse({
            "type": "authors",
            "items": serializer.data
        }, safe=False)


@swagger_auto_schema(tags=['Authors'], methods=["GET", "PUT"])
@api_view(['GET', 'PUT'])
def api_author(request, author_id):
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({"error": "Author not found", "success": False}, status=404)
    if request.method == 'GET':
        author_object = Author.objects.get(id=author_id)
        serialized_author = AuthorSerializer(
            instance=author_object, context={'request': request})
        return JsonResponse(serialized_author.data)
    elif request.method == 'PUT':
        author_object = Author.objects.get(id=author_id)
        serialized_author = AuthorSerializer(
            instance=author_object, data=request.data, context={'request': request})
        if serialized_author.is_valid():
            serialized_author.save()
            return JsonResponse(serialized_author.data, status=200)
        return JsonResponse({"success": False}, status=400)


def api_external_author(request, author_url):
    author_url = author_url.rstrip('/')
    try_author_object = get_author_object(author_url)
    if try_author_object is not None:
        serialized_author = AuthorSerializer(
            instance=try_author_object, context={'request': request})
        return JsonResponse(serialized_author.data)
    if request.method == 'GET':
        author_url = unquote(author_url)
        author_url += "/"
        parsed_uri = urlparse(author_url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if Node.objects.filter(baseUrl=result).exists():
            node_obj = Node.objects.get(baseUrl=result)
            auth = HTTPBasicAuth(node_obj.ourUsername,
                                 node_obj.ourPassword)
            

            try:
                print("Author url:", author_url)
                response = requests.get(author_url, auth=auth)
                print("Response text:", response.text)
                print("Response:", response.json())
                return JsonResponse(response.json(), status=response.status_code)
            
            except:
                response = requests.get(author_url, auth=auth)
                print("Author url:", author_url[:-1])
                response = requests.get(author_url[:-1], auth=auth)
                print("Response text:", response.text)
                return JsonResponse(response.json(), status=response.status_code)

            
            
            
    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


@swagger_auto_schema(tags=['Authors'], methods=["GET"])
@api_view(['GET'])
def api_followers(request, author_id):
    if request.method == 'GET':
        if Author.objects.filter(id=author_id).exists():
            author_object = Author.objects.get(id=author_id)
            following_objects = Following.objects.filter(
                author=author_object)
            following_authors = Author.objects.filter(
                id__in=following_objects.values("following_author_id"))
            serialized_followers = AuthorSerializer(
                instance=following_authors, context={'request': request}, many=True)
            return JsonResponse({"type": "followers", "items": serialized_followers.data}, safe=False)
        return JsonResponse({"error": "Author not found", "success": False}, status=404)


@swagger_auto_schema(tags=['Authors'], methods=["GET", "PUT", "DELETE"])
@api_view(['GET', 'PUT', "DELETE"])
def api_follower(request, author_id, author_url):
    following_author_object = get_author_object(author_url)

    if request.method == 'GET':
        if following_author_object is None:

            return JsonResponse({"status": "stranger", "success": False}, status=404)

        # The object
        followed_author_object = Author.objects.get(id=author_id)

        follow_request_object = FollowRequest.objects.filter(
            requester=following_author_object, receiver=followed_author_object)

        if follow_request_object.exists():
            return JsonResponse({"status": "pending", "success": False}, status=404)

        following_objects = Following.objects.filter(author=followed_author_object,
                                                     following_author=following_author_object)

        if following_objects.exists():
            actor_object = AuthorSerializer(instance=following_author_object, context={
                                            'request': request}).data
            actor_object["id"] = author_url
            actor_display_name = actor_object["displayName"]
            return JsonResponse({
                "type": "follow",
                "summary": f"{actor_display_name} followed {followed_author_object.displayName}",
                "actor": actor_object,
                "object": AuthorSerializer(instance=followed_author_object, context={'request': request}).data
            }, safe=False)

        return JsonResponse({"error": "Follower not found", "success": False}, status=404)

    elif request.method == 'PUT':
        if following_author_object is None:
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        data = request.data

        obj = request.data

        # The object
        followed_author_object = Author.objects.get(id=author_id)
        if data.get("areFriends") is not None:
            following_objects = Following.objects.filter(
                author=followed_author_object, following_author=following_author_object)

            if following_objects.exists():
                following_object = following_objects.first()
                following_object.areFriends = data.get("areFriends")
                reverse_following_object = Following.objects.create(author=following_author_object,
                                                                    following_author=followed_author_object, areFriends=True)
                following_object.save()
                reverse_following_object.save()
                return JsonResponse({"success": True}, status=200)

            return JsonResponse({"error": "Follower not found", "success": False}, status=404)

        if Following.objects.filter(author=followed_author_object, following_author=following_author_object).exists():
            return JsonResponse({"error": "Already following", "success": False}, status=400)

        if request.data.get("accepted") == False:
            follow_request_object = FollowRequest.objects.get(
                requester=following_author_object, receiver=followed_author_object)

            follow_request_content_type = ContentType.objects.get_for_model(
                follow_request_object)

            notification_item = NotificationItem.objects.filter(
                content_type=follow_request_content_type, object_id=follow_request_object.id).first()

            if notification_item:
                notification_item.delete()

            follow_request_object.delete()
            return JsonResponse({"success": True}, status=200)

        # accept
        following_object = Following.objects.create(author=followed_author_object,
                                                    following_author=following_author_object)

        # LOCAL FOLLOW
        reverse_following_object = Following.objects.filter(
            author=following_author_object, following_author=followed_author_object).exists()

        if reverse_following_object:
            reverse_following_object = Following.objects.get(
                author=following_author_object, following_author=followed_author_object)
            following_object.areFriends = True
            reverse_following_object.areFriends = True
            following_object.save()
            reverse_following_object.save()

        # REMOTE FOLLOW
        message = {}
        if following_author_object.isExternalAuthor:
            foreign_author_url = following_author_object.url
            node = Node.objects.filter(
                baseUrl=following_author_object.host.rstrip('/')+"/")
            if node.exists():
                node = node.first()
                auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
                response = requests.get(
                    foreign_author_url.rstrip('/') + "/followers/" + str(followed_author_object.url), auth=auth, headers={"origin": request.META["HTTP_HOST"]})
                if response.status_code == 200:
                    following_object.areFriends = True
                    reverse_following_objects = Following.objects.filter(author=following_author_object,
                                                                         following_author=followed_author_object)
                    if reverse_following_objects.exists():
                        reverse_following_objects.update(areFriends=True)
                        reverse_following_object.save()
                    else:
                        reverse_following_object = Following.objects.create(author=following_author_object,
                                                                            following_author=followed_author_object)

                    following_object.save()

                # No matter what, we send a follow response object
                response = requests.post(foreign_author_url.rstrip('/') + "/inbox",
                                         auth=auth,
                                         json=obj, headers={"origin": request.META["HTTP_HOST"]})
                try:
                    message = response.json()
                except:
                    return HttpResponse(response.text, status=response.status_code)
            else:
                return JsonResponse({"error": "Node not found", "success": False}, status=404)

        # Delete Notification
        follow_request_object = FollowRequest.objects.get(
            requester=following_author_object, receiver=followed_author_object)

        follow_request_content_type = ContentType.objects.get_for_model(
            follow_request_object)

        notification_item = NotificationItem.objects.filter(
            content_type=follow_request_content_type, object_id=follow_request_object.id).first()

        if notification_item:
            notification_item.delete()

        follow_request_object.delete()

        return JsonResponse(message, safe=False, status=200)

    elif request.method == 'DELETE':
        if following_author_object is None:
            return JsonResponse({"error": "Author not found", "success": False}, status=404)

        followed_author_object = Author.objects.get(id=author_id)

        following_objects = Following.objects.filter(
            author=followed_author_object, following_author=following_author_object)

        if following_objects.exists():
            following_objects.delete()
        else:
            return JsonResponse({"error": "Follower not found", "success": False}, status=404)

        reverse_following_object = Following.objects.filter(
            author=following_author_object, following_author=followed_author_object)
        if reverse_following_object.exists():
            reverse_following_object = reverse_following_object.first()
            reverse_following_object.areFriends = False
            reverse_following_object.save()

        # Remote unfollow notifcation
        if followed_author_object.isExternalAuthor:
            node = Node.objects.filter(
                baseUrl=followed_author_object.host.rstrip('/')+"/")
            if node.exists():
                node = node.first()
                auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
                data = {
                    "type": "Unfollow",
                    "summary": f"{following_author_object.displayName} wants to unfollow {followed_author_object.displayName}",
                    "actor": AuthorSerializer(instance=following_author_object, context={'request': request}).data,
                    "object": AuthorSerializer(instance=followed_author_object, context={'request': request}).data
                }
                response = requests.post(
                    followed_author_object.url.rstrip("/") + "/inbox", auth=auth, headers={"origin": request.META["HTTP_HOST"]}, json=data)
                if response.status_code >= 400:
                    return JsonResponse({"error": "Successfully sent an unfollow request to the external authors", "success": False}, status=response.status_code)
                else:
                    return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"error": "Invalid request", "success": False}, status=405)


@swagger_auto_schema(tags=['Authors'], methods=["GET"])
@api_view(['GET'])
def api_liked(request, author_id):
    if request.method == 'GET':
        if Author.objects.filter(id=author_id).exists():

            author_object = Author.objects.get(id=author_id)

            liked_posts = LikePost.objects.filter(author=author_object)
            liked_comments = LikeComment.objects.filter(author=author_object)

            serialized_liked = LikePostSerializer(
                instance=liked_posts, context={'request': request}, many=True)

            serialized_liked_comments = LikeCommentSerializer(
                instance=liked_comments, context={'request': request}, many=True)

            serialized_liked = list(
                chain(serialized_liked.data, serialized_liked_comments.data))

            return JsonResponse({"type": "liked", "items": serialized_liked}, safe=False)

        return JsonResponse({"error": "Author not found", "success": False}, status=404)


def api_discover(request):
    if request.method == 'GET':
        author_dicts = []

        #local_author = Author.objects.filter(
        #    Q(isExternalAuthor=False) & ~Q(url="") & ~Q(url=None) &Q(allowRegister=True))

        #author_dicts = AuthorSerializer(
        #    instance=local_author, context={'request': request}, many=True).data

        nodes = Node.objects.all()
        for node in nodes:
            if node.baseUrl == "https://deadly-bird-justin-ce5a27ea0b51.herokuapp.com/":
                auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
                response = requests.get(
                    node.baseUrl + node.service + "/authors/", auth=auth, headers={"origin": request.META["HTTP_HOST"]})
                if response.status_code == 200:
                    items = response.json()["items"]
                    
                    for item in items:
                        flag = False
                        for dict in author_dicts:
                            if dict["url"] == item["url"]:
                                flag = True
                                break
                        if not flag:
                            author_dicts.append(item)

        
        print("Author_dicts:", author_dicts)
        return JsonResponse(
            {
                "type": "authors",
                "items": author_dicts
            }, status=200, safe=False)


@api_view(['POST'])
def api_make_friends(request, author_id, author_url):
    author_url = unquote(author_url)
    if request.method == 'POST':
        following_author_object = get_author_object(author_url)
        if following_author_object is None:
            return JsonResponse({"error": "Author not found", "success": False}, status=404)
        followed_author_object = Author.objects.get(id=author_id)
        following_objects = Following.objects.filter(
            author=followed_author_object, following_author=following_author_object)
        if following_objects.exists():
            following_objects.update(areFriends=True)
            reverse_following_object = Following.objects.filter(author=following_author_object,
                                                                following_author=followed_author_object)
            if reverse_following_object.exists():
                reverse_following_object.update(areFriends=True)
            else:
                reverse_following_object = Following.objects.create(author=following_author_object,
                                                                    following_author=followed_author_object, areFriends=True)
            return JsonResponse({"success": True}, status=200)
        return JsonResponse({"error": "Follower not found", "success": False}, status=404)
    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


@api_view(['POST'])
def api_handle_decline(request, author_id):
    if request.method == 'POST':
        data = request.data

        receiver = get_author_object(data["actor"]["id"])
        requester = get_author_object(data["object"]["id"])

        if FollowRequest.objects.filter(requester=requester, receiver=receiver).exists():
            FollowRequest.objects.filter(
                requester=requester, receiver=receiver).delete()

            if requester.isExternalAuthor:
                node = Node.objects.filter(
                    baseUrl=requester.host.rstrip('/')+"/")
                if node.exists():
                    node = node.first()
                    auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)

                    response = requests.post(
                        requester.url.rstrip('/') + "/inbox", auth=auth, headers={"origin": request.META["HTTP_HOST"]}, json=data)

                    if response.status_code != 200 and response.status_code != 201:
                        return JsonResponse({"error": "Failed to send follow response to external authors", "success": False}, status=500)

            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"error": "Follow request not found", "success": False}, status=404)
    else:
        return JsonResponse({"error": "Method not Allowed", "success": False}, status=405)
