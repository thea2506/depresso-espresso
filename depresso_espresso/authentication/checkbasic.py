import base64
from .models import Node
from http.client import HTTPSConnection
from base64 import b64encode


#Reference: https://stackoverflow.com/questions/46426683/django-basic-auth-for-one-view-avoid-middleware from meshy accessed 3/11/2024
# def checkBasic(request):
#     ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''
#     auth_header = request.META.get('HTTP_AUTHORIZATION', '')
#     token_type, _, credentials = auth_header.partition(' ')
#     username, password = base64.b64decode(credentials).split(':')
#     print("NODE CHECKBASSICCCCCCCCCCCCCCCCC1", username, password)
#     node = Node.objects.get(theirusername=username, theirpassword=password)
#     print("NODE CHECKBASSICCCCCCCCCCCCCCCCC2", node)
#     return node

def checkBasic(request):
    ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')
    username, password = base64.b64decode(credentials).split(':')
    print("NODE CHECKBASSICCCCCCCCCCCCCCCCC1", username, password)
    node = Node.objects.get(theirusername=username, theirpassword=password)
    print("NODE CHECKBASSICCCCCCCCCCCCCCCCC2", node)
    return node

# def basic_auth(username, password):
#     token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
#     return f'Basic {token}'

# username = "user_name"
# password = "password"

# #This sets up the https connection
# c = HTTPSConnection("www.google.com")
# #then connect
# headers = { 'Authorization' : basic_auth(username, password) }
# c.request('GET', '/', headers=headers)
# #get the response back
# res = c.getresponse()
# # at this point you could check the status etc
# # this gets the page text
# data = res.read()  