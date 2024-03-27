from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, FollowRequest, Following
from authentication.serializers import AuthorSerializer
from inbox.models import Notification, NotificationItem
from inbox.serializers import NotificationSerializer, NotificationItemSerializer
from django.contrib.contenttypes.models import ContentType
from urllib.parse import urlparse
from posts.models import Post, Comment, LikeComment, LikePost
from posts.serializers import PostSerializer, CommentSerializer
from authors.views import get_author_object
import uuid
from drf_yasg.utils import swagger_auto_schema
from utils import Pagination


@swagger_auto_schema(tags=['Inbox'], methods=["GET", "POST", "DELETE"])
@api_view(['GET', 'POST', "DELETE"])
def api_inbox(request, author_id):

    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    if request.method == 'GET':
        author_object = Author.objects.get(id=author_id)

        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        notification_items = NotificationItem.objects.filter(
            notification=notification_object).order_by('id')

        paginator = Pagination("inbox")
        page = paginator.paginate_queryset(notification_items, request)
        serializer = NotificationItemSerializer(
            page, context={'request': request}, many=True)

        return JsonResponse({'type': 'inbox', 'items': serializer.data}, status=200)

    elif request.method == 'POST':
        type = request.data.get('type').lower()
        if type == 'follow':
            return handle_follow(request, author_id)
        if type == 'followresponse':
            return handle_follow_response(request, author_id)
        if type == 'like':
            return handle_like(request, author_id)
        if type == 'comment':
            return handle_comment(request, author_id)
        if type == 'post':
            return handle_post(request, author_id)
        if type == 'share':
            return handle_share(request, author_id)

    elif request.method == 'DELETE':
        author_object = Author.objects.get(id=author_id)

        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        notification_object.items.all().delete()

        return JsonResponse({'success': 'Inbox cleared'}, status=200)


def handle_follow(request, author_id):
    actor_obj = request.data.get('actor')
    actor_url = actor_obj['url']
    normalized_actor_url = actor_url.replace("127.0.0.1", "localhost")

    if not Author.objects.filter(url=actor_url).exists() and not Author.objects.filter(
            url=normalized_actor_url).exists():
        old_id = actor_obj.get('id')
        old_id = old_id.rstrip("/").split("/")[-1]
        print("The old id", old_id)
        actor_obj["id"] = old_id
        actor_obj["isExternalAuthor"] = True
        actor_obj["username"] = uuid.uuid4()
        print("This shit runs")
        serializer = AuthorSerializer(
            data=actor_obj, context={"request": request})
        if serializer.is_valid():
            print("Valid")
            actor = serializer.save(id=uuid.UUID(
                old_id), username=uuid.uuid4(), isExternalAuthor=True)
            print(actor.id)
        else:
            return JsonResponse(serializer.errors, status=500)

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


def handle_follow_response(request, author_id):
    print("INBOX ITEM RECEIVED", request.data)

    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    author_object = Author.objects.get(id=author_id)

    data = request.data

    actor = request.data.get('actor')
    object = request.data.get('object')
    accepted = request.data.get('accepted')

    following_author_object = Author.objects.filter(id=author_id)
    if not following_author_object.exists():
        print("AUTHOR LOCAL NOT EXISTS")
        return HttpResponse(status=404)

    if accepted == True:
        # Handle Accept
        actor_object = Author.objects.filter(url=actor['url'].rstrip("/"))
        if not actor_object.exists():
            actor_object = Author.objects.filter(
                url=actor['url'].rstrip("/") + "/")

            if not actor_object.exists():
                old_id = actor.get('id')
                old_id = old_id.rstrip("/").split("/")[-1]
                print("The old id", old_id)
                actor["id"] = old_id
                actor["isExternalAuthor"] = True
                actor["username"] = uuid.uuid4()
                print("This shit runs")
                serializer = AuthorSerializer(
                    data=actor, context={"request": request})
                if serializer.is_valid():
                    print("Valid")
                    actor_object = serializer.save(id=uuid.UUID(
                        old_id), username=uuid.uuid4(), isExternalAuthor=True)
                    print("FOREIGN OBJECT CREATED", actor_object.id)
                else:
                    return JsonResponse(serializer.errors, status=500)

            else:
                actor_object = actor_object.first()

        else:
            actor_object = actor_object.first()

        print(actor_object.id)
        following_author_object = following_author_object.first()
        # Now we have actor
        following_objects = Following.objects.filter(
            author=actor_object, following_author=following_author_object)

        if following_objects.exists():
            print("Already following")
            return JsonResponse({'success': 'Followed'}, status=201)

        else:
            print("CREATE NEW")
            following_object = Following.objects.create(
                author=actor_object, following_author=following_author_object)

            reverse_following_objects = Following.objects.filter(
                author=following_author_object, following_author=actor_object)

            if reverse_following_objects.exists():
                print("FRIEND")
                reverse_following_object = reverse_following_objects.first()
                reverse_following_object.areFriends = True
                reverse_following_object.save()
                following_object.areFriends = True
                following_object.save()

            else:
                print("NOT FRIEND")

            return JsonResponse({'success': 'Followed'}, status=201)

    else:
        # Handle Reject
        print("REJECTION FROM THEIR END")

        # Delete Notification
        follow_request_object = FollowRequest.objects.filter(
            requester=following_author_object, receiver=actor_object)

        if follow_request_object.exists():
            print("Follow Request Exists")
            follow_request_object = follow_request_object.first()

            follow_request_content_type = ContentType.objects.get_for_model(
                follow_request_object)

            notification_item = NotificationItem.objects.filter(
                content_type=follow_request_content_type, object_id=follow_request_object.id).first()

            if notification_item:
                notification_item.delete()

            follow_request_object.delete()
        print("REACHING HERE")
        return JsonResponse({'success': 'Rejected'}, status=201)


def handle_like(request, author_id):
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    author_object = Author.objects.get(id=author_id)

    data = request.data

    liking_author_object = get_author_object(data.get('author')['url'])

    if "comments" in data.get('object'):
        comment_id = data.get('object').split('/')[-1]

        comment = Comment.objects.filter(id=comment_id)

        if comment.exists():  # Local comment
            comment = comment.first()
            like_comment_object = LikeComment.objects.filter(
                author=liking_author_object, comment=comment)

            if like_comment_object.exists():
                return JsonResponse({'error': 'Already liked'}, status=400)

            else:
                like_comment_object = LikeComment.objects.create(
                    author=liking_author_object, comment=comment)

                notification_object = Notification.objects.get_or_create(author=author_object)[
                    0]

                create_notification_item(
                    notification_object, object_instance=like_comment_object)

                return send_notification_item(request, notification_object)

        else:  # External comment
            like_comment_object = LikeComment.objects.create(
                author=liking_author_object, comment_url=data.get('object'))

            notification_object = Notification.objects.get_or_create(author=author_object)[
                0]

            create_notification_item(
                notification_object, object_instance=like_comment_object)

            return send_notification_item(request, notification_object)

    else:
        post_id = data.get('object').split('/')[-1]

        like_post_object = LikePost.objects.filter(
            author=liking_author_object, post=Post.objects.get(id=post_id))

        if like_post_object.exists():
            return JsonResponse({'error': 'Already liked'}, status=400)

        else:
            like_post_object = LikePost.objects.create(
                author=liking_author_object, post=Post.objects.get(id=post_id))

            notification_object = Notification.objects.get_or_create(author=author_object)[
                0]

            create_notification_item(
                notification_object, object_instance=like_post_object)

            return send_notification_item(request, notification_object)


def handle_comment(request, author_id):
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    author_object = Author.objects.get(id=author_id)

    data = request.data

    post_id = data.get('id').split('/')[-3]

    data['post'] = Post.objects.get(id=post_id).id

    serializer = CommentSerializer(
        data=data, context={"request": request}
    )

    if serializer.is_valid():
        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        if Comment.objects.filter(id=data.get('id').split('/')[-1]).exists():
            comment_object = Comment.objects.get(
                id=data.get('id').split('/')[-1])
        else:
            comment_object = serializer.save()

        create_notification_item(
            notification_object, object_instance=comment_object)

        return send_notification_item(request, notification_object)
    else:
        return JsonResponse(serializer.errors, status=400)


def handle_post(request, author_id):
    if not Author.objects.filter(id=author_id).exists():
        return JsonResponse({'error': 'Author not found'}, status=404)

    author_object = Author.objects.get(id=author_id)

    data = request.data
    if not Author.objects.filter(url=data.get("author").get("url")).exists():
        Author.objects.create(isExternalAuthor=True, username=uuid.uuid4(), displayName=data.get("author").get("displayName"),
                              url=data.get("author").get("url"), type="author", host=data.get("author").get('host'), github=data.get("author").get("Github"),
                              profileImage=data.get("author").get("profileImage"), allowRegister=False)
        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

    serializer = PostSerializer(
        data=data, context={"request": request}
    )

    if serializer.is_valid():

        new_post = serializer.save()
        new_post.id = data.get('id').rstrip("/").split('/')[-1]
        new_post.save()

        notification_object = Notification.objects.get_or_create(author=author_object)[
            0]

        create_notification_item(
            notification_object, object_url=data.get('id'), content_type=ContentType.objects.get_for_model(Post))

        return send_notification_item(request, notification_object)
    else:
        return JsonResponse(serializer.errors, status=400)


def handle_share(request, author_id):
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


def create_notification_item(notification_object, object_instance=None, object_url=None, content_type=None):
    if object_instance:
        content_type = ContentType.objects.get_for_model(object_instance)
        notification_item_object = NotificationItem.objects.create(
            content_type=content_type, object_id=object_instance.id, content_object=object_instance)
    else:
        notification_item_object = NotificationItem.objects.create(content_type=content_type,
                                                                   object_url=object_url)

    notification_object.items.add(notification_item_object)


def send_notification_item(request, notification_object):
    notification_serializer = NotificationSerializer(
        instance=notification_object, context={'request': request})
    return JsonResponse(notification_serializer.data, status=201)
