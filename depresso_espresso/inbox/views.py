from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Author, FollowRequest
from authentication.serializers import AuthorSerializer


@api_view(['GET', 'POST', "DELETE"])
def api_inbox(request, author_id):
    if request.method == 'GET':
        return JsonResponse({'message': 'Inbox API'})
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
    if not Author.objects.filter(url=actor_url).exists():
        print("New external user")
        actor_obj.pop('id', None)
        actor = AuthorSerializer(data=actor_obj, context={'request': request})
        if actor.is_valid():
            actor.save()
        else:
            return JsonResponse({'error': 'Invalid actor'}, status=400)

    actor = Author.objects.get(url=actor_url)
    author = Author.objects.get(id=author_id)
    FollowRequest.objects.create(requester=actor, receiver=author)
    return JsonResponse({'message': 'Follow request sent'}, status=201)


def handle_like(request, author_id):
    pass


def handle_comment(request, author_id):
    pass


def handle_post(request, author_id):
    pass


def handle_share(request, author_id):
    pass
