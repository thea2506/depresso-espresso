import base64
from .models import Node

#Reference: https://stackoverflow.com/questions/46426683/django-basic-auth-for-one-view-avoid-middleware from meshy accessed 3/11/2024
def checkBasic(request):
    ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
    node = Node.objects.get(ourUsername=decoded_credentials[0], ourPassword=decoded_credentials[1])

    return node
