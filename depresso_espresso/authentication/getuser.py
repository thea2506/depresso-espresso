from .models import Author
from django.contrib.sessions.models import Session


def getUser(request):
    ''' This function gets the currently authenticated user based on session information'''
    if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)
          return(user)
      
    return(None)

   