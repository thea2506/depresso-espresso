from urllib.parse import urlparse
from django.shortcuts import render
from .models import Notification, NotificationItem
from authentication.models import Author, Following
from posts.models import Comment, Like, Post
import json
import requests
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers as django_serializers
from posts.views import utility_get_posts
from .serializers import *
from posts.serializers import *
from django.contrib.contenttypes.models import ContentType
from authentication.serializer import *
from authentication.checkbasic import my_authenticate


def create_notification(request):
    data = json.loads(request.body)
    type = data['type']
    author = Author.objects.get(id=data["sender_id"])

    # like / comment / share
    if "receiver_id" in data:
        Notification.objects.create(
            sender_id=author.id, type=type, receiver_id=data["receiver_id"], post_id=data["post_id"])
    # post
    elif "post_id" in data:
        Notification.objects.create(
            sender_id=author.id, type=type, post_id=data["post_id"])
    return HttpResponse("Notification created")


def get_notifications(request, authorid):
    data = []

    # like / comment
    notifications = Notification.objects.filter(receiver_id=authorid)
    for notification in notifications:
        author = Author.objects.get(id=notification.sender_id)
        if Post.objects.filter(id=notification.post_id).exists():
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
                "post": {
                    "id": post.id,
                    "authorid": post.author.id,
                },
                "created_at": notification.created_at,
                "type": notification.type,
            })

    # share/post
    follow_list = Following.objects.filter(authorid=authorid)
    for each in follow_list:
        notifications_post = Notification.objects.filter(
            type="post", sender_id=each.followingid)
        notifications_share = Notification.objects.filter(
            type="share", sender_id=each.followingid)

        notifications = [*notifications_post, *notifications_share]
        for notification in notifications:
            author = Author.objects.get(id=notification.sender_id)
            if notification.created_at > each.created_at and Post.objects.filter(id=notification.post_id).exists():
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

                    "post": {
                        "id": post.id,
                        "authorid": post.author.id,
                    },
                    "created_at": notification.created_at,
                    "type": notification.type,
                })
    return JsonResponse(data, safe=False)


@api_view(["POST", "GET"])
def handle_inbox(request, authorid):
    """ LOCAL REMOTE
        GET /authors/<str:authorid>/inbox: This retrieves all posts that would be sent to this author's inbox
        POST /authors/<str:authorid>/inbox This is where other authors post relevant information that this author needs to know about"""

    if request.method == "GET":  # Get all posts from authorid's inbox

        user = Author.objects.get(id=authorid)
        all_visible_posts = utility_get_posts(authorid)  # Get all public posts

        # JUST POSTS FOR NOW
        data = {
            "type": "inbox",
            "author": user.id,
            "items": json.loads(django_serializers.serialize('json', all_visible_posts))
        }
        return JsonResponse(data)

    # An author could be sent a relevant post, follow, like, or comment that the inbox must handle.
    if request.method == "POST":
        # get the type of message sent to the inbox
        type = request.POST.get("type")
        match type:
            case "Post":  # Author's friend/follower makes a post that this author is interested in. It seems that external posts will not be knows by our server until one arrives in any of our author's inboxes.

                # check if post exists in db already (Post should only not exist already if it originates from an external author)
                if Post.objects.filter(url=request.data["id"]).exists():
                    return JsonResponse({"message": "Post already exists in db, no action required"}, status=200)

                # --- Anything beyond this point is meant to handle posts from external authors ---

                if Author.objects.filter(url=request.POST.get("author")["url"]).exists():
                    # get author of post if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)
                    external_author = Author.objects.get(
                        url=request.POST.get("author")["url"])

                else:  # Create new author if this author doesn't exist

                    external_author = Author.objects.create()
                    if not external_author:
                        return JsonResponse({"message": "Error creating new author"})
                    external_author.host = request.POST.get("author")["host"]
                    external_author.displayName = request.POST.get("author")[
                        "displayName"]
                    external_author.url = request.POST.get("author")["url"]
                    external_author.username = request.POST.get("author")["id"]
                    external_author.isExternalAuthor = True

                data = {  # Send this data as a post request to our internal new_external_post function in posts/views.py
                    "title":  request.POST.get("title"),
                    "id": request.POST.get("id"),
                    "origin": request.POST.get("origin"),
                    "description": request.POST.get("description"),
                    "visibility": request.POST.get("visibility"),
                    "contentType": request.POST.get("contentType"),
                    "content": request.POST.get("content"),
                    "author": external_author.id
                }

                # Create a new post object in db
                response = requests.post('/new_post', data)
                if response["success"] == False:
                    return JsonResponse({"message": "Failed to create a post on server"}, status=500)

            case "Follow":  # Some external user sends a follow request to this author

                # Check if the requesting author already exists in our db
                if Author.objects.filter(url=request.data["actor"]["url"]).exists():
                    # get author of request if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)
                    external_author = Author.objects.get(
                        url=request.data["actor"]["url"])

                else:
                    host = request.POST.get("actor")["host"]
                    displayName = request.POST.get("actor")[
                        "displayName"]
                    url = request.POST.get("actor")["url"]
                    username = request.POST.get("actor")["id"]

                    Author.objects.create(
                        host=host, displayName=displayName, url=url, username=username, isExternalAuthor=True)

                if not Author.objects.filter(url=request.POST.get("object")["url"]).exists():
                    return JsonResponse({"message": "The author specified in 'object' field does not exist"})

                else:
                    local_author = Author.objects.get(
                        url=request.POST.get("object")["url"])

                data = {  # Send this data as a post request to our internal create_external_follow_request function in authorprofile/views.py
                    "localid":  local_author.id,
                    "externalid": external_author.id
                }

                response = requests.post(
                    '/create_external_follow_request/', data)

            # TODO:
            case "Like":  # Some user likes this author's post
                pass
            case  "Comment":
                pass
            case _:
                pass


def get_friends(authorid):
    '''LOCAL
    Get all friends of an author'''

    friends = Following.objects.filter(authorid=authorid, areFriends=True)
    data = []
    for friend in friends:
        user = Author.objects.get(id=friend.authorid)
        data.append(user)

    return data


def get_followings(authorid):
    ''' LOCAL
      Get all authors that an author is following'''

    following = Following.objects.filter(authorid=authorid)
    data = []
    for follow in following:
        user = Author.objects.get(id=follow.followingid)
        data.append(user)
    return data


def api_inbox(request, authorid):
    user = my_authenticate(request)
    if user is None:
        return JsonResponse({"message": "User not authenticated"}, status=401)

    if not Author.objects.filter(id=authorid).exists():
        return JsonResponse({"message": "Author does not exist", "success": False}, status=404)
    author_object = Author.objects.get(id=authorid)

    # LOCAL + REMOTE
    if request.method == "POST":
        if not isinstance(user, Author):
            return JsonResponse({"message": "Local users only"}, status=401)

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
