import base64
from django.contrib.sessions.models import Session
from .models import Author, Node
import uuid

# Reference: https://stackoverflow.com/questions/46426683/django-basic-auth-for-one-view-avoid-middleware from meshy accessed 3/11/2024


def check_basic(request):
    ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''

    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith("Basic "):
        return None

    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(
        encoded_credentials).decode("utf-8").split(':')
    username = decoded_credentials[0]
    password = decoded_credentials[1]
    if not username or not password:
        return None

    try:
        # uri = request.headers['Origin'] + "/"
        node = Node.objects.filter(
            theirUsername=decoded_credentials[0], theirPassword=decoded_credentials[1])

    except Node.DoesNotExist:
        return None

    return Author(id=uuid.uuid4(), username=node.baseUrl, isExternalAuthor=True)


def my_authenticate(request):
    ''' This function checks if a request is from a node that is allowed to connect with our node (it has the correct username and password)'''

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')

            if not Author.objects.filter(id=uid).exists():
                user = check_basic(request)
                if not user:
                    return None
            else:
                user = Author.objects.get(id=uid)
    else:
        user = check_basic(request)
        if not user:
            return None

    return user
