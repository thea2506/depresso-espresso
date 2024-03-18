from django.shortcuts import render
from .models import Notification
from authentication.models import Author, Following
from posts.models import Post
from django import forms
import json, requests
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers

def create_notification(request):
    data = json.loads(request.body)
    type = data['type']
    author = Author.objects.get(id=data["sender_id"])
    
    # like / comment / share
    if "receiver_id" in data:
        Notification.objects.create(sender_id=author.id, type=type, receiver_id=data["receiver_id"], post_id=data["post_id"])
    # post
    elif "post_id" in data:
        Notification.objects.create(sender_id=author.id, type=type, post_id=data["post_id"])
    return HttpResponse("Notification created")

def get_notifications(request, authorid):
    data = []

    # like / comment
    notifications = Notification.objects.filter(receiver_id=authorid)
    for notification in notifications:
        author = Author.objects.get(id=notification.sender_id)
        if Post.objects.filter(id=notification.post_id).exists():
            post = Post.objects.get(id=notification.post_id)
            data.append({
                "author": {
                    "id": author.id,
                    "displayName": author.displayName,
                    "url": author.url,
                    "host": author.host,
                    "github": author.github,
                    "profileImage": author.profileImage,
                },
                "post" : {
                    "id": post.id,
                    "authorid": post.author.id, 
                },
                "created_at": notification.created_at,
                "type": notification.type,
            }) 

    # share/post
    follow_list = Following.objects.filter(authorid=authorid)
    for each in follow_list:
        notifications_post = Notification.objects.filter(type="post", sender_id=each.followingid)
        notifications_share = Notification.objects.filter(type="share", sender_id=each.followingid)

        notifications = [*notifications_post, *notifications_share]
        for notification in notifications:
            author = Author.objects.get(id=notification.sender_id)
            if notification.created_at > each.created_at and Post.objects.filter(id=notification.post_id).exists():
                post = Post.objects.get(id=notification.post_id)
                data.append({
                    "author": {
                        "id": author.id,
                        "displayName": author.displayName,
                        "url": author.url,
                        "host": author.host,
                        "github": author.github,
                        "profileImage": author.profileImage,
                    },

                    "post" : {
                        "id": post.id,
                        "authorid": post.author.id, 
                    },
                    "created_at": notification.created_at,
                    "type": notification.type,
                })
    return JsonResponse(data, safe=False)

@api_view(["POST", "GET"])
def handle_inbox(request, authorid):
    """ LOCAL REMOTE
        GET /authors/<str:authorid>/inbox: This retrieves all posts that would be sent to this author's inbox
        POST /authors/<str:authorid>/inbox This is where other authors post relevant information that this author needs to know about"""
    
    if request.method == "GET": # Get all posts from authorid's inbox

        user = Author.objects.get(id=authorid)
        # Author's inbox should contain posts from friends and followed authors
        items = []

        if len(request.data) > 0:
            following_authors = requests.get(user.url + '/following/') # Get the authors that this user is folowing
            for author in (following_authors):
                author_ob = Author.objects.get(id = author) # Get the author object of the friend
                following_posts = Post.objects.filter(author = author_ob, visibility = "PUBLIC")
                items.append(serializers.serialize('json', following_posts))

        
        friends = requests.get( user.url + '/friends/') # Get the author's friends
        for friend in (friends.json()):
             author_ob = Author.objects.get(id = friend["id"]) # Get the author object of the friend
             friend_posts = Post.objects.filter(author = author_ob, visibility = "FRIENDS")
             items.append(serializers.serialize('json', friend_posts))


        if items == ['[]']:
            items = []
        else:
            #Reference: https://note.nkmk.me/en/python-dict-list-sort/ Accessed 3/16/2024
            sorted(items, key=lambda x: x.published) # sort the posts by date
        
        data = {
                "type": "inbox",
                "author": user.id,
                "items": items
        }
        return JsonResponse(data)





    if request.method == "POST": # An author could be sent a relevant post, follow, like, or comment that the inbox must handle.
        type = request.POST.get("type") # get the type of message sent to the inbox
        match type:
             case "Post": # Author's friend/follower makes a post that this author is interested in. It seems that external posts will not be knows by our server until one arrives in any of our author's inboxes.

                if Post.objects.filter(url=request.data["id"]).exists(): # check if post exists in db already (Post should only not exist already if it originates from an external author)
                     return JsonResponse({"message": "Post already exists in db, no action required"}, status = 200)
                
                # --- Anything beyond this point is meant to handle posts from external authors ---
                     
                if Author.objects.filter(url=request.POST.get("author")["url"]).exists():
                    external_author = Author.objects.get(url=request.POST.get("author")["url"]) # get author of post if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)

                else: # Create new author if this author doesn't exist
                     
                    external_author = Author.objects.create()
                    if not external_author:
                        return JsonResponse({"message": "Error creating new author"})
                    external_author.host = request.POST.get("author")["host"]
                    external_author.displayName = request.POST.get("author")["displayName"]
                    external_author.url = request.POST.get("author")["url"]
                    external_author.username = request.POST.get("author")["id"]
                    external_author.isExternalAuthor = True
                    
                data = { # Send this data as a post request to our internal new_external_post function in posts/views.py
                    "title":  request.POST.get("title"),
                    "id": request.POST.get("id"),
                    "origin": request.POST.get("origin"),
                    "description": request.POST.get("description"),
                    "visibility": request.POST.get("visibility"),
                    "contentType": request.POST.get("contentType"),
                    "content": request.POST.get("content"),
                    "author": external_author.id
                }

                response = requests.post('/new_post', data) # Create a new post object in db
                if response["success"] == False:
                     return JsonResponse({"message": "Failed to create a post on server"}, status=500)


             case "Follow": # Some external user sends a follow request to this author
                  
                if Author.objects.filter(url=request.data["actor"]["url"]).exists(): # Check if the requesting author already exists in our db
                    external_author = Author.objects.get(url=request.data["actor"]["url"]) # get author of request if they already exist in the db (Compare url instead of id because the incoming request data format should contain the author's entire url as an id which is incompatible with our database)
                    
                else:
                    external_author = Author.objects.create()
                    if not external_author:
                        return JsonResponse({"message": "Error creating new author"})
                    external_author.host = request.POST.get("actor")["host"]
                    external_author.displayName = request.POST.get("actor")["displayName"]
                    external_author.url = request.POST.get("actor")["url"]
                    external_author.username = request.POST.get("actor")["id"]
                    external_author.isExternalAuthor = True

                if not Author.objects.filter(url=request.POST.get("object")["url"]).exists():
                     return JsonResponse({"message": "The author specified in 'object' field does not exist"})
                
                else:
                     local_author = Author.objects.get(url=request.POST.get("object")["url"])
                     
                    
                data = { # Send this data as a post request to our internal create_external_follow_request function in authorprofile/views.py
                "localid":  local_author.id,
                "externalid": external_author.id
                    }
                
                response = requests.post('/create_external_follow_request/', data)

             #TODO:
             case "Like": # Some user likes this author's post
                  pass
             case  "Comment":
                  pass
             case _:
                  pass
                  


