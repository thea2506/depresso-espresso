from urllib.parse import urlparse
from django.shortcuts import render
from .models import Notification, NotificationItem
from authentication.models import Author, Following
from posts.models import Comment, Like, Post
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers as django_serializers
from posts.views import utility_get_posts
from .serializers import *
from posts.serializers import *
from django.contrib.contenttypes.models import ContentType
from authentication.serializer import *
from authentication.checkbasic import my_authenticate


def api_inbox(request, authorid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author does not exist", "success": False}, status=404)
    author_object = Author.objects.get(id=authorid)

    # LOCAL + REMOTE
    if request.method == "POST":
        # if not isinstance(user, Author):
        #     return JsonResponse({"message": "Local users only"}, status=401)

        data = json.loads(request.body)
        if "type" not in data:
            return JsonResponse({"message": "Type not specified", "success": False}, status=400)
        type = data["type"].lower()
        print(type)
        if type == "like":
            print("like")
            return create_like_notification(request, author_object, data)
        elif type == "follow":
            return create_follow_notification(request, author_object, data)
        elif type == "post":
            return create_post_notification(request, author_object, data)
        elif type == "comment":
            return create_comment_notification(request, author_object, data)

    # LOCAL + REMOTE
    elif request.method == "GET":
        if not Notification.objects.filter(author=author_object).exists():
            return JsonResponse({"message": "No notifications", "success": True}, status=200)

        author_object = Author.objects.get(id=authorid)

        notifications_object = Notification.objects.get(
            author=author_object)
        notification_items = NotificationItem.objects.filter(
            notification=notifications_object)

        data = NotificationItemSerializer(
            instance=notification_items, many=True, context={"request": request}).data

        return JsonResponse({
            "type": "inbox",
            "author": author_object.url,
            "items": data
        }, safe=False, status=200)

    # LOCAL
    elif request.method == "DELETE":
        if not isinstance(user, Author):
            return JsonResponse({"message": "Local users only"}, status=401)

        if not Notification.objects.filter(author=author_object).exists():
            return JsonResponse({"message": "No notifications to delete", "success": True}, status=200)

        author_object = Author.objects.get(id=authorid)

        notifications_object = Notification.objects.get(
            author=author_object)
        notification_items = NotificationItem.objects.filter(
            notification=notifications_object)

        for notification_item in notification_items:
            notification_item.delete()

        notifications_object.delete()

        return JsonResponse({"message": "Notifications deleted", "success": True}, status=200)
    else:
        return JsonResponse({"message": "Method not allowed", "success": False}, status=405)


def create_like_notification(request, author_object, data):
    object_url = urlparse(data["object"])
    object_segments = object_url.path.split("/")

    # like comment
    if "comments" in object_segments:
        post_id = object_segments[len(object_segments) - 3]
        comment_id = object_segments[len(object_segments) - 1]
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
    # like post
    else:
        post_id = object_segments[len(object_segments) - 1]
        post = Post.objects.get(id=post_id)
        comment = None

    author_json = AuthorSerializer(instance=author_object, context={
                                   "request": request}).data

    # create notification
    notification_object = Notification.objects.get_or_create(
        author=author_object)[0]

    if Like.objects.filter(author=data["author"], post=post, comment=comment).exists():
        like_object = Like.objects.get(
            author=data["author"], post=post, comment=comment)
        content_type = ContentType.objects.get_for_model(like_object)
        for notification_item in notification_object.items.all():
            if notification_item.content_type == content_type and notification_item.object_id == like_object.id:
                notification_object.items.remove(notification_item)
                notification_item.delete()
        like_object.delete()
        return JsonResponse({"message": "Like notification deleted", "success": True}, status=200)

    like_object = Like.objects.create(
        author=data["author"], post=post, comment=comment)

    create_notification_item(notification_object, like_object)
    return send_notification_serializer_response(notification_object, request)


def create_comment_notification(request, author_object, data):
    parsed_url = urlparse(data["id"])
    path_segments = parsed_url.path.split("/")
    comment_id = path_segments[path_segments.index("comments") + 1]
    comment_object = Comment.objects.get(id=comment_id)
    serializer = CommentSerializer(
        instance=comment_object, data=data, context={"request": request}
    )

    if serializer.is_valid():
        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]
        create_notification_item(notification_object, comment_object)
        return send_notification_serializer_response(notification_object, request)
    else:
        return JsonResponse(serializer.errors, status=404)


def create_post_notification(request, author_object, data):
    post_url = urlparse(data["id"])
    post_segments = post_url.path.split("/")
    post_id = post_segments[len(post_segments) - 1]
    post_object = Post.objects.get(id=post_id)
    serializer = PostSerializer(
        instance=post_object, data=data, context={"request": request}
    )

    if serializer.is_valid():

        notification_object = Notification.objects.get_or_create(
            author=author_object)[0]
        create_notification_item(notification_object, post_object)
        return send_notification_serializer_response(notification_object, request)
    else:
        return JsonResponse(serializer.errors, status=400)


def create_share_notification(request, author_object, data):
    pass


def create_follow_notification(request, author_object, data):
    follow_object = Follow.objects.create(
        id=uuid.uuid4(),
        object=author_object,
        actor=data["actor"]
    )
    follow_serializer = FollowSerializer(
        instance=follow_object, data=data, context={"request": request}
    )

    if follow_serializer.is_valid():
        follow_instance = follow_serializer.save()
        notification_object = Notification.objects.get_or_create(
            author=author_object)[0]
        create_notification_item(notification_object, follow_instance)
        return send_notification_serializer_response(notification_object, request)
    else:
        return JsonResponse(follow_serializer.errors, status=400)


def send_notification_serializer_response(notification_object, request):
    inbox_serializer = NotificationSerializer(
        instance=notification_object, context={"request": request}
    )
    return JsonResponse(inbox_serializer.data, status=201)


def create_notification_item(notification, content=None, json_data=None):
    if content:
        content_type = ContentType.objects.get_for_model(content)
        inbox_item_object = NotificationItem.objects.create(content_type=content_type,
                                                            object_id=content.id,
                                                            content_object=content)
    else:
        inbox_item_object = NotificationItem.objects.create(
            json_data=json_data)

    notification.items.add(inbox_item_object)
