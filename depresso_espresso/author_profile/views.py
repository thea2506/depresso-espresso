from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from posts.models import Post
from authentication.models import Author, Following, FollowRequest, Node
from rest_framework.decorators import api_view
from authentication.checkbasic import checkBasic
from django.core import serializers
import requests
from django.contrib.sessions.models import Session
import json


@api_view(["GET","PUT"])
def author_profile(request, authorid):
    ''' LOCAL and REMOTE GET ://service/authors/{AUTHOR_ID}: Returns the profile information for authorid
        LOCAL PUT ://service/authors/{AUTHOR_ID}: Updates the profile information for authorid'''

    if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)

    if request.method == "PUT": # Update user profile information
        if user.is_authenticated == True:
          author = get_object_or_404(Author, pk=authorid)
          data = json.loads(request.body)
          if user == author:
            if data.get('displayName') != None:
              author.displayName = data['displayName']
            if data.get('github') != None:
              author.github = data['github']
            if data.get('profileImage') != None:
              author.profileImage = data['profileImage']
            author.save()
            return JsonResponse({"message": "Profile updated successfully"})

    if request.method == "GET": # Gets user profile information
        if user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
        
        if not Author.objects.filter(id=authorid).exists():
          return JsonResponse({"message": "Author not found"}, status= 500)
        
        author = Author.objects.get(id=authorid)

        data = {
          
              "type": "author",
              "id": author.id,
              "url": author.url,
              "host": author.host,
              "displayName": author.displayName,
              "github": author.github,
              "profileImage": author.profileImage
            
        }

        return JsonResponse(data)
        
    else:
       return render(request, "index.html")


@api_view(['GET'])
def get_authors(request):
  ''' LOCAL and REMOTE
      Handles getting all LOCAL authors on our server with and without an optional search parameter
      GET ://service/authors/ or GET ://service/authors?page=10&size=5'''
  
  if request.session.session_key is not None:

          session = Session.objects.get(session_key=request.session.session_key)
          if session:
              session_data = session.get_decoded()
              uid = session_data.get('_auth_user_id')
              user = Author.objects.get(id=uid)


  if request.method == "GET":


    if user.is_authenticated == False:
          #handle retreiving authors for an external server (only retreive our LOCALLY CREATED authors)
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
          authors = Author.objects.filter(isExternalAuthor = False) # Only send the external server our locally created authors

          items = []
          for author in authors:
            items.append({
               
              "type": author.type,
              "id": author.id,
              "url": author.url,
              "host": author.host,
              "displayName": author.displayName,
              "username": author.username,
              "github": author.github,
              "profileImage": author.profileImage

            })
    else:

      # Poll all external nodes for their authors
      nodes = Node.objects.all()
      for node in nodes:
        username = node["theirUsername"]
        password = node["theirPassword"]
        baseUrl = node["baseUrl"]
        authors = requests.get(baseUrl + '/authors/', auth=(username, password)) # send get request to node to retrieve external author info

        for author in authors["items"]:
           
          if not Author.objects.filter(url=author["url"]).exists(): # Check if the author already exists in our db
              # if author does not exist, create a new one
              new_author = Author.objects.create()
              if not new_author:
                  return JsonResponse({"message": "Error creating new author"})
              new_author.host = author["host"]
              new_author.displayName = author["displayName"]
              new_author.url = author["url"]
              new_author.username = author["username"]
              new_author.isExternalAuthor = True

      search_terms = request.GET.get('search')

      if search_terms:
        authors = Author.objects.filter(displayName__icontains=search_terms)

      else:
        authors = Author.objects.all()
      
      items = []
      for author in authors:
        items.append({
            
          "type": author.type,
          "id": author.id,
          "url": author.url,
          "host": author.host,
          "displayName": author.displayName,
          "username": author.username,
          "github": author.github,
          "profileImage": author.profileImage

        })

    data = {
       "type": "author",
       "items": items
    }
  
    return JsonResponse(data, safe=False)
   


@api_view(['GET'])
def get_followers(request, authorid):
  ''' LOCAL and REMOTE   
      GET ://service/authors/{AUTHOR_ID}/followers: Get all followers of an author'''
  
  user = Author.objects.get(id=authorid)
  
  if request.method == "GET":

    if user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
    followers = Following.objects.filter(followingid=authorid)
    items = []
    data = {}

    for follower in followers:
      user = Author.objects.get(id=follower.authorid)
      items.append({
        "type": user.type,
        "id": user.id,
        "url": user.url,
        "host": user.host,
        "displayName": user.displayName,
        "username": user.username,
        "github": user.github,
        "profileImage": user.profileImage
      })

      data = {"type": "followers", "items": items}

    return JsonResponse(data, safe=False)
  else:
    return JsonResponse({"message": "Method not allowed"}, status=405)


@api_view(['GET', 'DELETE', 'PUT'])  
def handle_follow(request, authorid, foreignid):
    ''' LOCAL AND REMOTE GET ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        LOCAL PUT ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        LOCAL DELETE ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Unfollow another author'''

    if request.session.session_key is not None:
          session = Session.objects.get(session_key=request.session.session_key)
          if session:
              session_data = session.get_decoded()
              uid = session_data.get('_auth_user_id')
              user = Author.objects.get(id=uid)
              authorid = user.id

    foreign_author = Author.objects.get(id = foreignid)
    author = Author.objects.get(id = authorid)
   
    if request.method == "GET": #check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
       if user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
       if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          return JsonResponse({"success": True})
          
       else:
          return JsonResponse({"success": False})
      
    if request.method == "PUT": # Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)

      if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          Following.objects.filter(authorid = foreignid, followingid = authorid).update(areFriends = True)
          Following.objects.create(authorid = authorid, followingid = foreignid, areFriends = True)
          message = "Follow request from", foreign_author.id, "accepted by", author.displayName, "and they are now friends" 

      return JsonResponse({"message": message,"success": True})
       
      
    if request.method == "DELETE": #  remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID      

      if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
        message = foreign_author.displayName, "unfollowed", author.displayName 
       
        if Following.objects.filter(authorid = foreignid, followingid = authorid).areFriends:
          Following.objects.filter(authorid = authorid, followingid = foreignid).update(areFriends = False)
          Following.objects.filter(authorid = foreignid, followingid = authorid).update(areFriends = False)
          message = foreign_author.displayName, "unfollowed", author.displayName, "and they are no longer friends"
      
        Following.objects.filter(authorid = authorid, followingid = foreignid).delete()    
  
        return JsonResponse({"message": message,"success": True})
      

@api_view(['POST'])  
def create_follow_request(request, foreignid):
    '''LOCAL
      Pipeline: 
      author ON OUR SERVER clicks the follow button on another author's profile (LOCAL or REMOTE author) -->
      frontend sends request to /create_follow_request/ -->
      create new FollowRequest object in db -->
      if requested author is remote, send to their inbox using their url field and basic auth info from their node
      if requested author is local, do nothing else because i don't think there is any benefit in sending local events to local inboxes "'''

    # Front end will send the data format to our server and other server as well. Frontend handles the data format.
    # All data of the foreign author is sent to the backend as a dictionary so we do not need to request for their info

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

            
    if request.method == 'POST':
       # I think the external author that our author is attempting to follow should already exist on our db at this point, or else they wouldn't be able to see their profile
      
      # if not exist, create an Author object for the foreign author
     # if  not Author.objects.filter(id = foreignid).exists():         
      #    Author.object.create(id = foreign_author_info["id"], host = foreign_author_info["host"], displayName = foreign_author_info["displayName"], url = foreign_author_info["url"], github = foreign_author_info["github"], profileImage = foreign_author_info["profileImage"])

      foreign_author = Author.objects.get(id=foreignid)

      # follow logic
      if Following.objects.filter(authorid = user.id, followingid = foreignid).exists(): 
        message = "You are already following this author"
        return JsonResponse({"message": message, "success": False}, status=405)

      elif FollowRequest.objects.filter(requester = user.id, receiver = foreignid).exists():
        message = user["displayName"], "has already sent a follow request to", foreign_author.displayName
        return JsonResponse({"message": message, "success": False}, status=405)
      
      elif not FollowRequest.objects.filter(requester = user.id, receiver = foreignid).exists():

        FollowRequest.objects.create(requester = user.id, receiver = foreignid)

        data = {
           
              "type": "Follow",      
              "summary": foreign_author.displayName + " has unfollowed " + user.displayName,
              "actor":{"type": "author",
                      "id": foreign_author.id,
                      "url": foreign_author.url,
                      "host": foreign_author.host,
                      "displayName": foreign_author.displayName,
                      "github": foreign_author.github,
                      "profileImage": foreign_author.profileImage
              },
              "object":{
                      "type": "author",
                      "id": user.id,
                      "url": user.url,
                      "host": user.host,
                      "displayName": user.displayName,
                      "github": user.github,
                      "profileImage": user.profileImage
              }
          }
        
        # Check if the author that the user wants to follow is from an external node:
        host = foreign_author.host   # get the host from the id
        
        if Node.objects.filter(baseUrl = host).exists():
          node = Node.objects.get(baseUrl = host)
          username = node["theirUsername"]
          password = node["theirPassword"]
          response = requests.post(foreign_author.url + '/inbox/', data,  auth=(username,password)) # Send data to external author's inbox

          if response.status != 200:
              return JsonResponse({"message": "Could not sent request to external node", "success": False}, status=response.status)
        
        message = user.displayName, "sent a follow request to", foreign_author.displayName   
        return JsonResponse({"message": message, "success": True})

@api_view(['POST'])     
def create_external_follow_request(request):
   """LOCAL
      creates a follow request that had originated from an external author to one of our local authors
      Pipeline:
      author on external node clicks the follow button on one of our author's profiles -->
      Remote server sends follow event to our author's local inbox -->
      Within inbox, If remote author is unknown to our db, create new author (maybe add way to update remote profile if it changes) -->
      Inbox sends POST request to this function to create the new follow request object
      """
   
   if request.method == 'POST':
      localid = request.data.get("localid")
      externalid = request.data.get("externalid")
      FollowRequest.objects.create(requester = externalid, receiver = localid)

      return JsonResponse({"message": "Request created successfully"})




@api_view(['PUT']) 
def respond_to_follow_request(request, foreignid):
    ''' LOCAL/REMOTE 
        Respond to a follow request from another author'''
    
    # Foreign author should exist in our database, since we created it when the follow request was sent
    foreign_author = Author.objects.get(id=foreignid)

    if request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        if data["decision"] == "accept":
          FollowRequest.objects.filter(requester = foreign_author.id, receiver = user.id).delete()

          if Following.objects.filter(authorid = user.id, followingid = foreignid).exists():
            Following.objects.filter(authorid = user.id, followingid = foreignid).update(areFriends = True)
            Following.objects.create(authorid = foreignid, followingid = user.id, areFriends = True)
          else:
            Following.objects.create(authorid = foreignid, followingid = user.id, areFriends = False)
          message = "Follow request accepted"
          #foreign_author_follow(request, authorid, foreignid)
      
        elif data["decision"] == "decline":
          FollowRequest.objects.filter(requester = foreignid, receiver = user.id).delete()
          message = "Follow request declined"
        return JsonResponse({"message": message,"success": True})
        
    return JsonResponse({"message": "Error responding to follow request",})

@api_view(['GET']) 
def get_friends(request, authorid):
  ''' LOCAL
      Get all friends of an author'''
  
  if request.method == "GET":
    friends = Following.objects.filter(authorid=authorid, areFriends=True)
    data = []
    for friend in friends:
      user = Author.objects.get(id=friend.authorid.id)
      data.append({
        "type": user.type,
        "id": user.id,
        "url": user.url,
        "host": user.host,
        "displayName": user.displayName,
        "username": user.username,
        "github": user.github,
        "profileImage": user.profileImage
      })
    return JsonResponse(data, safe=False)
  else:
    return JsonResponse({"message": "Method not allowed"}, status=405)
  
def get_follow_list(request):
  ''' LOCAL
      Get all authors that an author is following'''
  
  if request.method == "GET":
    following = Following.objects.filter(authorid=request.user.id)
    data = []
    for follow in following:
      user = Author.objects.get(id=follow.followingid)
      data.append({
        "type": "author",
        "id": user.id,
        "url": user.url,
        "host": user.host,
        "displayName": user.displayName,
        "username": user.username,
        "github": user.github,
        "profileImage": user.profileImage,
        "friend" : follow.areFriends,
        "followedFrom": follow.created_at,
      })
    return JsonResponse({"data" : data, "success": True }, safe=False)
  else:
    return JsonResponse({"message": "Method not allowed"}, status=405)


def check_follow_status(request):
  '''Check the follow status between two authors'''

  data = request.GET
  authorid = data["id"]
  author = Author.objects.get(id=authorid)

  result = {}

  if request.method == "GET":
    # follow
    if Following.objects.filter(authorid = request.user.id, followingid = author.id).exists():
      if Following.objects.filter(authorid = request.user.id, followingid = author.id)[0].areFriends:
        result["status"] = "friend"
      else:
        result["status"] = "follower"
    
    # follow pending
    elif FollowRequest.objects.filter(requester = request.user.id, receiver = author.id).exists():
      result["status"] = "pending"
    
    # not following
    else:
      result["status"] = "stranger"
    result["success"] = True
    return JsonResponse(result)
  else:
    return JsonResponse({"success" : False})


def front_end_inbox(request, authorid):
    return render(request, 'index.html')

def get_follow_requests(request): # Can this be extended to be inbox?
    '''Get all follow requests for an author'''

    if request.method == "GET":
      authorid = request.GET.get("id")
      if authorid:
        follow_requests = FollowRequest.objects.filter(receiver=authorid)
        requesters = []
        for follow_request in follow_requests:
          # include logic here that checks if requester has an external host
          requester = Author.objects.get(id=follow_request.requester)
          requesters.append(requester)

        res = serializers.serialize("json", requesters, fields=["profileImage", "username", "github", "displayName", "url"])
        
        return HttpResponse(res, content_type="application/json")
      return JsonResponse({"message": "No new requests"})

def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})

def front_end(request, authorid):
    return render(request, 'index.html')

def get_image(request, image_file):
    return redirect(f'/images/{image_file}')
