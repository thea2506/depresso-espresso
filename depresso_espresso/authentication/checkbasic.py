import base64
from .models import Node


def checkBasic(request):
    ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''
#Reference: https://stackoverflow.com/questions/46426683/django-basic-auth-for-one-view-avoid-middleware from meshy accessed 3/11/2024
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')
    username, password = base64.b64decode(credentials).split(':')
    node = Node.objects.get(username=username, password=password)
    return node