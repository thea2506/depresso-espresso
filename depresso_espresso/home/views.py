from django.shortcuts import render
from .userstream import StreamView
from .search import SearchView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from authentication.models import Author, Following, FollowRequest, Node
from posts.models import Post
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
from django.core import serializers
import json


class StreamView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, "index.html")

# Create your views here.

def stream(request):
    rend = StreamView().get(request)
    return rend


@api_view(["POST", "GET"])
def handle_inbox(request, authorid):
    """ LOCAL REMOTE
        GET /authors/<str:authorid>/inbox: This retrieves all posts that would be sent to this author's inbox
        POST /authors/<str:authorid>/inbox This is where other authors post relevant information that this author needs to know about"""
    
    '''
    if request.session.session_key is not None: # Check if user is athenticated and get current user
                session = Session.objects.get(session_key=request.session.session_key)
                print("Session:", session)
                if session:
                    session_data = session.get_decoded()
                    uid = session_data.get('_auth_user_id')
                    user = Author.objects.get(id=uid)
                    if user.id != authorid:
                         return JsonResponse({"message": "Illegal inbox access"}, status = 401)
    '''

    if request.method == "GET": # Get all posts from authorid's inbox
        print("Method Get\n")
        user = Author.objects.get(id=authorid)
        print("user:", user.displayName)

        # Author's inbox should contain posts from friends and followed authors
        items = []
        print("lllllllaaaaaaaaaaaaaaaaaaaaaaaaaa", request.data)

        if len(request.data) > 0:
            following_authors = requests.get(user.url + '/following/') # Get the authors that this user is folowing
            print("following authors:", following_authors.json())
            for author in (following_authors):
                print("AUTHOR:  ", author)
                author_ob = Author.objects.get(id = author) # Get the author object of the friend
                following_posts = Post.objects.filter(author = author_ob, visibility = "PUBLIC")
                items.append(serializers.serialize('json', following_posts))

        
        friends = requests.get( user.url + '/friends/') # Get the author's friends
        print("friends:", friends.json())
        for friend in (friends.json()):
             author_ob = Author.objects.get(id = friend["id"]) # Get the author object of the friend
             friend_posts = Post.objects.filter(author = author_ob, visibility = "FRIENDS")
             items.append(serializers.serialize('json', friend_posts))

        if items == ['[]']:

            items = []

        # Reference: https://note.nkmk.me/en/python-dict-list-sort/ Accessed 3/16/2024
        # sorted(items, key=lambda x: x["fields"]["published"]) # sort the posts by date
        
        print("\n\nITEMS:", items)
        data = {
                "type": "inbox",
                "author": user.id,
                "items": items
        }

        return JsonResponse(data)


    if request.method == "POST": # An author could be sent a relevant post, follow, like, or comment that the inbox must handle.
        
        type = request.data["type"] # get the type of message sent to the inbox

        match type:
             case "Post": # Author's friend/follower makes a post that this author is interested in. It seems that external posts will not be knows by our server until one arrives in any of our author's inboxes.

                if Post.objects.filter(url=request.data["id"]).exists(): # check if post exists in db already (Post should only not exist already if it originates from an external author)
                     return JsonResponse({"message": "Post already exists in db, no action required"}, status = 200)
                

                # --- Anything beyond this point is meant to handle posts from external authors ---
                     
                if Author.objects.filter(url=request.data["author"]["url"]).exists():
                    external_author = Author.objects.get(url=request.data["author"]["url"]) # get author of post if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)

                else: # Create new author if this author doesn't exist
                     
                    external_author = Author.objects.create()
                    if not external_author:
                        return JsonResponse({"message": "Error creating new author"})
                    external_author.host = request.data["author"]["host"]
                    external_author.displayName = request.data["author"]["displayName"]
                    external_author.url = request.data["author"]["url"]
                    external_author.username = request.data["author"]["id"]
                    external_author.isExternalAuthor = True
                    
                data = { # Send this data as a post request to our internal new_external_post function in posts/views.py
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
                if response["success"] == False:
                     return JsonResponse({"message": "Failed to create a post on server"}, status=500)


             case "Follow": # Some external user sends a follow request to this author
                  
                if Author.objects.filter(url=request.data["actor"]["url"]).exists(): # Check if the requesting author already exists in our db
                    external_author = Author.objects.get(url=request.data["actor"]["url"]) # get author of request if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)
                    
                else:
                    external_author = Author.objects.create()
                    if not external_author:
                        return JsonResponse({"message": "Error creating new author"})
                    external_author.host = request.data["actor"]["host"]
                    external_author.displayName = request.data["actor"]["displayName"]
                    external_author.url = request.data["actor"]["url"]
                    external_author.username = request.data["actor"]["id"]
                    external_author.isExternalAuthor = True

                if not Author.objects.filter(url=request.data["object"]["url"]).exists():
                     return JsonResponse({"message": "The author specified in 'object' field does not exist"})
                
                else:
                     local_author = Author.objects.get(url=request.data["object"]["url"])
                     
                    
                data = { # Send this data as a post request to our internal create_external_follow_request function in authorprofile/views.py
                "localid":  local_author.id,
                "externalid": external_author.id
                    }
                
                response = requests.post('/create_external_follow_request/', data)

             case "Like": # Some user likes this author's post
                  pass
             case  "Comment":
                  pass
             case _:
                  pass
                  




