from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from posts.models import Post
from authentication.models import Author
from django.core.serializers import serialize
import json

# Potentially edit this to only use 1 function
def get_profile(request, authorid):
    if request.method == "GET":
        author = get_object_or_404(Author, pk=authorid)
        data = {
            "type": "author",
            "id": f"http://{request.get_host()}/authors/{authorid}",
            "host": f"http://{request.get_host()}/",
            "displayName": author.display_name,
            "url": f"http://{request.get_host()}/authors/{authorid}",
            "github": author.github_link,
            "profileImage": author.profile_image
        }
        return JsonResponse(data)

def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})

def front_end(request, authorid):
    return render(request, 'index.html')

def get_image(request, image_file):
    return redirect(f'/images/{image_file}')