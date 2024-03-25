from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, Following, FollowRequest
from authentication.serializers import AuthorSerializer
from inbox.models import Notification, NotificationItem
from django.contrib.contenttypes.models import ContentType
from depresso_espresso.constants import *
from requests.auth import HTTPBasicAuth
import requests
from urllib.parse import unquote


def get_author_object(author_url):
    author_url = unquote(author_url)
    normalized_author_url = author_url.replace("127.0.0.1", "localhost")
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
    if request.method == 'GET':
        author_url = unquote(author_url)
        basic = HTTPBasicAuth(MY_NODE_USERNAME, MY_NODE_PASSWORD)
        response = requests.get(author_url, auth=basic)
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

        # The object
        followed_author_object = Author.objects.get(id=author_id)

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

        Following.objects.create(author=followed_author_object,
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
