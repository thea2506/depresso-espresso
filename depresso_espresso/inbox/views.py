from django.shortcuts import render
from .models import Notification
from authentication.models import Author, Following
from posts.models import Post
from django import forms
import json
from django.http import HttpResponse, JsonResponse

def create_notification(request):
    data = json.loads(request.body)
    type = data['type']
    author = Author.objects.get(id=data["sender_id"])
    
    # like / comment / share
    if "receiver_id" in data:
        Notification.objects.create(sender_id=author.id, type=type, receiver_id=data["receiver_id"], post_id=data["post_id"])
    # post
    elif "post_id" in data:
        Notification.objects.create(sender_id=author.id, type=type, post_id=data["post_id"])
    return HttpResponse("Notification created")

def get_notifications(request, authorid):
    data = []
    
    # like/comment/share
    notifications = Notification.objects.filter(receiver_id=authorid)
    for notification in notifications:
        author = Author.objects.get(id=notification.sender_id)
        post = Post.objects.get(id=notification.post_id)
        data.append({
            "author": {
                "id": author.id,
                "displayName": author.displayName,
                "url": author.url,
                "host": author.host,
                "github": author.github,
                "profileImage": author.profileImage,
            },
            "post" : {
                "id": post.id,
            },
            "created_at": notification.created_at,
            "type": notification.type,
        }) 

    # post
    follow_list = Following.objects.filter(authorid=authorid)
    for each in follow_list:
        notifications = Notification.objects.filter(type="post", sender_id=each.followingid)
        print(notifications)
        for notification in notifications:
            author = Author.objects.get(id=notification.sender_id)
            post = Post.objects.get(id=notification.post_id)
            data.append({
                "author": {
                    "id": author.id,
                    "displayName": author.displayName,
                    "url": author.url,
                    "host": author.host,
                    "github": author.github,
                    "profileImage": author.profileImage,
                },

                "post" : {
                    "id": post.id,
                },
                "created_at": notification.created_at,
                "type": notification.type,
            })
    print(data)
    return JsonResponse(data, safe=False)
