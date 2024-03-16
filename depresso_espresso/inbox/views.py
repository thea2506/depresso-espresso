from django.shortcuts import render
from .models import Notification
from authentication.models import Author
from django import forms
import json
from django.http import HttpResponse, JsonResponse

def create_notification(request):
    data = json.loads(request.body)
    type = data['type']
    author = Author.objects.get(id=data["authorid"])

    message = ""

    if type == "post":
        message = f"{author.displayName} has made a new post"
    
    Notification.objects.create(author=author, message=message)
    return HttpResponse("Notification created")

def get_notifications(request, authorid):
    data = []
    
    notifications = Notification.objects.filter(author=authorid)
    for notification in notifications:
        data.append({
            "author": {
                "id": notification.author.id,
                "displayName": notification.author.displayName,
                "url": notification.author.url,
                "host": notification.author.host,
                "github": notification.author.github,
                "profileImage": notification.author.profileImage,
            },
            "message": notification.message,
            "created_at": notification.created_at,
        })
    return JsonResponse(data, safe=False)
