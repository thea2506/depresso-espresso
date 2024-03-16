from django.shortcuts import render
from .userstream import StreamView
from .search import SearchView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from authentication.models import Author, Following, FollowRequest, Node
from posts.models import Post
from rest_framework.decorators import api_view
from posts.views import new_post
from django.http import JsonResponse
import requests

'''
class StreamView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, "index.html")

# Create your views here.

@login_required
def stream(request):
    rend = StreamView().get(request)
    return rend
'''


@api_view(["POST"])
def handle_inbox(request):


    if request.session.session_key is not None: # Check if user is athenticated and get current user
                session = Session.objects.get(session_key=request.session.session_key)
                if session:
                    session_data = session.get_decoded()
                    uid = session_data.get('_auth_user_id')
                    user = Author.objects.get(id=uid)
                    authorid = user.id

    if request.method == "GET":
         pass


    if request.method == "POST":
        

        type = request.data["type"] # get the type of message sent to the inbox

        match type:
             case "Post": # Some user makes a post to this author

                if Post.objects.filter(url=request.data["id"]).exists(): # check if post exists in db already
                     return JsonResponse({"message": "Post already exists in db, no action required"})
                     
                if Author.objects.filter(url=request.data["author"]["url"]).exists():
                    author = Author.objects.get(url=request.data["author"]["url"]) # get author of post if they already exist in the db
                    if not author: # Create new author if this author doesn't exist (only applies if post originates from external author)
                        author = Author.objects.create()
                        if not author:
                            return JsonResponse({"message": "Error creating new author"})
                        
                        author.host = request.data["author"]["host"]
                        author.displayName = request.data["author"]["displayName"]
                        author.url = request.data["author"]["url"]
                        author.username = request.data["author"]["id"]
                        author.isExternalAuthor = True
                    
                data = { # Send this data as a post request to our internal new_post function in posts/views.py
                    "inbox": "Yes",
                    "title":  request.data["title"],
                    "id": request.data["id"],
                    "origin": request.data["origin"],
                    "description": request.data["description"],
                    "visibility": request.data["visibility"],
                    "contentType": request.data["contentType"],
                    "content": request.data["content"],
                    "author": author  
                }

                response = requests.post('/new_post/', data) # Create a new post object in db


             case "Follow": # Some user sends a follow request to this author
                  pass
             case "Like": # Some user likes this author's post
                  pass
             case  "Comment":
                  pass
             case _:
                  pass
                  




