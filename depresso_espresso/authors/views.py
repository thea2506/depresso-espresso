from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, Following
from authentication.serializers import AuthorSerializer
from depresso_espresso.constants import *
from requests.auth import HTTPBasicAuth
import requests
from urllib.parse import unquote


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
                following_author=author_object)
            following_authors = Author.objects.filter(
                id__in=following_objects.values("author_id"))
            serialized_followers = AuthorSerializer(
                instance=following_authors, context={'request': request}, many=True)
            return JsonResponse({"type": "followers", "items": serialized_followers.data}, safe=False)
        return JsonResponse({"error": "Author not found", "success": False}, status=404)


@api_view(['GET', 'PUT', "DELETE"])
def api_follower(request, author_id, author_url):
    author_url = unquote(author_url)
    if not Author.objects.filter(url=author_url).exists():
        return JsonResponse({"error": "Author not found", "success": False}, status=404)
    if request.method == 'GET':
        author_object = Author.objects.get(url=author_url)
        followed_author_object = Author.objects.get(id=author_id)
        following_objects = Following.objects.filter(author=author_object,
                                                     following_author=followed_author_object)
        if following_objects.exists():
            basic = HTTPBasicAuth(MY_NODE_USERNAME, MY_NODE_PASSWORD)
            response = requests.get(author_url, auth=basic)
            actor_object = response.json()
            actor_display_name = actor_object["displayName"]
            return JsonResponse({
                "type": "follow",
                "summary": f"{actor_display_name} followed {followed_author_object.displayName}",
                "actor": actor_object,
                "object": AuthorSerializer(instance=followed_author_object, context={'request': request}).data
            }, safe=False)

        return JsonResponse({"error": "Follower not found", "success": False}, status=404)
    return JsonResponse({"error": "Invalid request", "success": False}, status=405)
