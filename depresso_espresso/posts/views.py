from rest_framework.decorators import api_view
from django.http import JsonResponse
from authentication.checkbasic import my_authenticate
from posts.models import *
from posts.serializers import *


@api_view(['GET', 'POST'])
def api_posts(request, author_id):
    user = my_authenticate(request)
    if request.method == 'GET':
        posts = Post.objects.get(user.id)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = PostSerializer(
            data=data, context={"request": request})

        if serializer.is_valid():
            new_post = serializer.save()
            returned_data = PostSerializer(instance=new_post, context={
                                           "request": request}).data
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
        posts = Post.objects.filter(visibility="PUBLIC").order_by("-published")
        serializer = PostSerializer(
            posts, many=True, context={"request": request})
        return JsonResponse({"type": "posts", "items": serializer.data}, safe=False)
    else:
        return JsonResponse({"error": "Invalid request"}, status=405)
