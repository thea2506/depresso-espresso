from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, Following, FollowRequest
from authentication.serializers import AuthorSerializer
from inbox.models import Notification, NotificationItem
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


def get_author_object(author_url):
    author_url = unquote(author_url)
    if "127.0.0.1" in author_url:
        normalized_author_url = author_url.replace("127.0.0.1", "localhost")
    elif "localhost" in author_url:
        normalized_author_url = author_url.replace("localhost", "127.0.0.1")
    else:
        normalized_author_url = author_url
    if not Author.objects.filter(url=author_url).exists() and not Author.objects.filter(
            url=normalized_author_url).exists():
        return None
    if Author.objects.filter(url=author_url).exists():
        return Author.objects.get(url=author_url)
    return Author.objects.get(url=normalized_author_url)


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


@api_view(['GET'])
def api_external_author(request, author_url):
    id = author_url.split("/")[-1]
    if (Author.objects.filter(id=id).exists()):
        author_object = Author.objects.get(id=id)
        serialized_author = AuthorSerializer(
            instance=author_object, context={'request': request})
        return JsonResponse(serialized_author.data)
    if request.method == 'GET':
        author_url = unquote(author_url)
        parsed_uri = urlparse(author_url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        node_obj = Node.objects.get(baseUrl=result)
        auth = HTTPBasicAuth(node_obj.ourUsername,
                             node_obj.ourPassword)
        response = requests.get(author_url, auth=auth)
        return JsonResponse(response.json(), status=response.status_code)
    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


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

        if request.data.get("decision") == "decline":
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

        follow_request_object = FollowRequest.objects.get(
            requester=following_author_object, receiver=followed_author_object)

        follow_request_content_type = ContentType.objects.get_for_model(
            follow_request_object)

        notification_item = NotificationItem.objects.filter(
            content_type=follow_request_content_type, object_id=follow_request_object.id).first()

        if notification_item:
            notification_item.delete()

        follow_request_object.delete()

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
        if following_author_object.isExternalAuthor:
            foreign_author_url = following_author_object.url
            node = Node.objects.get(baseUrl=following_author_object.host)
            auth = HTTPBasicAuth(node.ourUsername, node.ourPassword)
            response = requests.get(
                foreign_author_url + "/followers/" + str(followed_author_object.url), auth=auth, headers={"origin": request.META["HTTP_HOST"]})
            print(response.status_code)
            if response.status_code == 200:
                print("Remote follow successful")
                following_object.areFriends = True
                reverse_following_object = Following.objects.create(author=following_author_object,
                                                                    following_author=followed_author_object, areFriends=True)
                following_object.save()
                reverse_following_object.save()
                response = requests.put(foreign_author_url + "/followers/" + str(followed_author_object.url),
                                        auth=auth,
                                        data={"areFriends": True}, headers={"origin": request.META["HTTP_HOST"]})
                print(response)

        return JsonResponse({"success": True}, status=200)

    elif request.method == 'DELETE':

        if following_author_object is None:
            return JsonResponse({"error": "Author not found", "success": False}, status=404)

        followed_author_object = Author.objects.get(id=author_id)

        following_objects = Following.objects.filter(
            author=followed_author_object, following_author=following_author_object)

        if following_objects.exists():
            following_objects.delete()
            return JsonResponse({"success": True}, status=200)

        return JsonResponse({"error": "Follower not found", "success": False}, status=404)

    return JsonResponse({"error": "Invalid request", "success": False}, status=405)


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
