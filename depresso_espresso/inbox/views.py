from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, FollowRequest
from authentication.serializers import AuthorSerializer
from inbox.models import Notification, NotificationItem
from inbox.serializers import NotificationSerializer, NotificationItemSerializer
from django.contrib.contenttypes.models import ContentType
from urllib.parse import urlparse
from posts.models import Post, Comment, LikeComment, LikePost
from posts.serializers import PostSerializer, CommentSerializer


@api_view(['GET', 'POST', "DELETE"])
def api_inbox(request, author_id):

    if request.method == 'GET':
        author_object = Author.objects.get(id=author_id)

        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        notification_items = NotificationItem.objects.filter(
            notification=notification_object).order_by('-id')

        print(notification_items)

        serializer = NotificationItemSerializer(
            notification_items, many=True, context={'request': request})

        return JsonResponse({'type': 'inbox', 'items': serializer.data}, status=200)

    elif request.method == 'POST':
        type = request.data.get('type').lower()
        if type == 'follow':
            return handle_follow(request, author_id)
        if type == 'like':
            return handle_like(request, author_id)
        if type == 'comment':
            return handle_comment(request, author_id)
        if type == 'post':
            return handle_post(request, author_id)
        if type == 'share':
            return handle_share(request, author_id)
    elif request.method == 'DELETE':
        pass


def handle_follow(request, author_id):
    actor_obj = request.data.get('actor')
    actor_url = actor_obj['url']
    normalized_actor_url = actor_url.replace("127.0.0.1", "localhost")

    if not Author.objects.filter(url=actor_url).exists() and not Author.objects.filter(
            url=normalized_actor_url).exists():

        actor_obj.pop('id', None)
        actor_obj["isExternalAuthor"] = True
        actor = AuthorSerializer(data=actor_obj, context={'request': request})
        if actor.is_valid():
            actor.save()
        else:
            return JsonResponse({'error': 'Invalid actor'}, status=400)

    if Author.objects.filter(url=actor_url).exists():
        actor = Author.objects.get(url=actor_url)
    else:
        actor = Author.objects.get(url=normalized_actor_url)

    author = Author.objects.get(id=author_id)
    follow_request_object = FollowRequest.objects.create(
        requester=actor, receiver=author)
    notification_object = Notification.objects.get_or_create(author=author)[0]
    create_notification_item(
        notification_object, object_instance=follow_request_object)
    return send_notification_item(request, notification_object)


def handle_like(request, author_id):
    pass


def handle_comment(request, author_id):
    pass


def handle_post(request, author_id):
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    author_object = Author.objects.get(id=author_id)

    data = request.data

    serializer = PostSerializer(
        data=data, context={"request": request}
    )

    if serializer.is_valid():
        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        create_notification_item(
            notification_object, object_url=data.get('id'), content_type=ContentType.objects.get_for_model(Post))

        return send_notification_item(request, notification_object)
    else:
        return JsonResponse(serializer.errors, status=400)


def handle_share(request, author_id):
    pass


def create_notification_item(notification_object, object_instance=None, object_url=None, content_type=None):
    if object_instance:
        content_type = ContentType.objects.get_for_model(object_instance)
        notification_item_object = NotificationItem.objects.create(
            content_type=content_type, object_id=object_instance.id, content_object=object_instance)
    else:
        print(">>>>>>>>>>", object_url)
        notification_item_object = NotificationItem.objects.create(content_type=content_type,
                                                                   object_url=object_url)

    notification_object.items.add(notification_item_object)


def send_notification_item(request, notification_object):
    notification_serializer = NotificationSerializer(
        instance=notification_object, context={'request': request})
    return JsonResponse(notification_serializer.data, status=201)
