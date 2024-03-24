from django.http import JsonResponse
from rest_framework.decorators import api_view


def api_inbox(request, author_id):
    return JsonResponse({'message': 'Inbox API'})
