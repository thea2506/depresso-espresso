from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from posts.models import Post
from authentication.models import Author, Following, FollowRequest, Node
from rest_framework.decorators import api_view
from authentication.checkbasic import checkBasic
import requests
from django.contrib.sessions.models import Session
import json
from django.views.decorators.http import require_http_methods



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

    if request.method == "PUT":
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

    if request.method == "GET":
        if user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
        if Author.objects.filter(id = authorid).exists():
          if request.META["HTTP_HOST"] in user.host: # if the author is saved on our server:
             author = Author.objects.filter(id = authorid)
             author_data = author.values()[0]
             
          else:
              split_id = authorid.split("authors")
              node = Node.objects.get(baseUrl = split_id[0]) # get the host from the id
              username = node["theirUsername"]
              password = node["theirPassword"]
              response = requests.get(authorid, auth=(username, password)) # send get request to node to retrieve external author info
              author_data = response.json()      
          
          data = {
             
                "type": "author",
                "id": author_data["id"],
                "url": author_data["url"],
                "host": author_data["host"],
                "displayName": author_data["displayName"],
                "github": author_data["github"],
                "profileImage": author_data["profileImage"]
              
          }

          return JsonResponse(data)
        
        else: 
           return JsonResponse({"message": "Author not found"}, status=404, safe=False)
        
    else:
       return render(request, "index.html")


@api_view(['GET'])
def get_authors(request):
  ''' LOCAL and REMOTE
      Handles getting all authors on the server with and without an optional search parameter
      GET ://service/authors/ or GET ://service/authors?page=10&size=5'''
  
  if request.method == "GET":

    if request.user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
    search_terms = request.GET.get('search')
    if search_terms:
      authors = Author.objects.filter(displayName__icontains=search_terms)
    else:
      authors = Author.objects.all() 

    data = []
    for author in authors:
      data.append({
        "type": author.type,
        "id": author.id,
        "url": author.url,
        "host": author.host,
        "displayName": author.displayName,
        "username": author.username,
        "github": author.github,
        "profileImage": author.profileImage
      })

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_followers(request, authorid):
  ''' LOCAL and REMOTE   
      GET ://service/authors/{AUTHOR_ID}/followers: Get all followers of an author'''
  
  if request.session.session_key is not None:
      session = Session.objects.get(session_key=request.session.session_key)
      if session:
          session_data = session.get_decoded()
          uid = session_data.get('_auth_user_id')
          user = Author.objects.get(id=uid)
  
  if request.method == "GET":

    if user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          

    followers = Following.objects.filter(followingid=authorid)
    items = []
    data = {}

    for follower in followers:
      user = Author.objects.get(id=follower.authorid.id)
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
def foreign_author_follow(request, authorid, foreignid):
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
    
    send_external = None

    if  Author.objects.filter(id = authorid).exists(): # if the foreign author is saved on our server:
        author = Author.objects.filter(id = author)
        author_data = author.values()[0]
      
             
    else:
        split_id = authorid.split("authors")
        node = Node.objects.get(baseUrl = split_id[0]) # get the host from the id
        username = node["theirUsername"]
        password = node["theirPassword"]
        response = requests.get(authorid, auth=(username, password)) # send get request to node to retrieve external author info
        author_data = response.json()
        send_external == "author"


    if request.META["HTTP_HOST"] in foreignid: # if the foreign author is saved on our server:
        foreign_author = Author.objects.get(id = foreignid)
        foreign_data = foreign_author.values()[0]
        
      
    else:
      split_id = foreignid.split("authors")
      node = Node.objects.get(baseUrl = split_id[0]) # get the host from the id
      username = node["theirUsername"]
      password = node["theirPassword"]
      response = requests.get(foreignid) # send get request to node to retrieve external author info
      send_external == "foreign"
      foreign_data = response.json()          

    if request.method == "GET": #check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
       if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
           
          data = {
             "type": "Follower",      
             "summary": foreign_data["displayName"] + " follows " + author_data["displayName"],
             "actor":{"type": "author",
                      "id": foreign_data["id"],
                      "url": foreign_data["url"],
                      "host": foreign_data["host"],
                      "displayName": foreign_data["displayName"],
                      "github": foreign_data["github"],
                      "profileImage": foreign_data["profileImage"]},
              "object":{
                      "type": "author",
                      "id": author_data["id"],
                      "url": author_data["url"],
                      "host": author_data["host"],
                      "displayName": author_data["displayName"],
                      "github": author_data["github"],
                      "profileImage": author_data["profileImage"]
              }
          }

          return JsonResponse(data)
          
       else:
          return JsonResponse({"message": "Follower does not exist"}, status=404)
      
    if request.method == "PUT": # Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)

      if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          Following.objects.filter(authorid = foreignid, followingid = authorid).update(areFriends = True)
          Following.objects.create(authorid = authorid, followingid = foreignid, areFriends = True)
          message = "Follow request from", foreign_data["displayName"], "accepted by", author_data["displayName"], "and they are now friends" 

          # Send a Friends message to foreign author's inbox:

          data = {
             "type": "Friends",      
             "summary": foreign_data["displayName"] + " is now friends with " + author_data["displayName"],
             "actor":{"type": "author",
                      "id": foreign_data["id"],
                      "url": foreign_data["url"],
                      "host": foreign_data["host"],
                      "displayName": foreign_data["displayName"],
                      "github": foreign_data["github"],
                      "profileImage": foreign_data["profileImage"]},
              "object":{
                      "type": "author",
                      "id": author_data["id"],
                      "url": author_data["url"],
                      "host": author_data["host"],
                      "displayName": author_data["displayName"],
                      "github": author_data["github"],
                      "profileImage": author_data["profileImage"]
              }
          }

      else:
          Following.objects.create(authorid = foreignid, followingid = authorid, areFriends = False)
          message = "Follow request from", foreign_author["displayName"], "accepted by", author_data["displayName"]

          # Send a Following message to foreign author's inbox:

          data = {
             "type": "Following",      
             "summary": foreign_data["displayName"] + " is now following " + author_data["displayName"],
             "actor":{"type": "author",
                      "id": foreign_data["id"],
                      "url": foreign_data["url"],
                      "host": foreign_data["host"],
                      "displayName": foreign_data["displayName"],
                      "github": foreign_data["github"],
                      "profileImage": foreign_data["profileImage"]},
              "object":{
                      "type": "author",
                      "id": author_data["id"],
                      "url": author_data["url"],
                      "host": author_data["host"],
                      "displayName": author_data["displayName"],
                      "github": author_data["github"],
                      "profileImage": author_data["profileImage"]
              }
          }

      if send_external == None:
            requests.post(foreignid + "/inbox", data) # data sent to local author's inbox
        
      elif send_external == "foreign":
        response = requests.post(foreignid +"/inbox", data, auth=(username, password)) # data sent to foreign author's inbox
        if response.status != 200:
            return JsonResponse({"message": "Could not sent request to external node", "success": False}, status=response.status)

      return JsonResponse({"message": message,"success": True})
       
      
    if request.method == "DELETE": #  remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID       

      if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
        message = foreign_data["displayName"], "unfollowed", author_data["displayName"] 

        data = {
              "type": "Unfollow",      
              "summary": foreign_data["displayName"] + " has unfollowed " + author_data["displayName"],
              "actor":{"type": "author",
                      "id": foreign_data["id"],
                      "url": foreign_data["url"],
                      "host": foreign_data["host"],
                      "displayName": foreign_data["displayName"],
                      "github": foreign_data["github"],
                      "profileImage": foreign_data["profileImage"]},
              "object":{
                      "type": "author",
                      "id": author_data["id"],
                      "url": author_data["url"],
                      "host": author_data["host"],
                      "displayName": author_data["displayName"],
                      "github": author_data["github"],
                      "profileImage": author_data["profileImage"]
              }
          }
        
        if send_external == None:
          requests.post(foreignid + "/inbox", data) # data sent to local author's inbox
      
        elif send_external == "foreign":
          response = requests.post(foreignid +"/inbox", data, auth=(username, password)) # data sent to foreign author's inbox
          if response.status != 200:
              return JsonResponse({"message": "Could not sent request to external node", "success": False}, status=response.status)
          
        elif send_external == "author":
           response = requests.post(authorid +"/inbox", data, auth=(username, password)) # data sent to author's inbox
           if response.status != 200:
              return JsonResponse({"message": "Could not sent request to external node", "success": False}, status=response.status)   

        if Following.objects.filter(authorid = foreignid, followingid = authorid).areFriends:
          Following.objects.filter(authorid = authorid, followingid = foreignid).update(areFriends = False)
          Following.objects.filter(authorid = foreignid, followingid = authorid).update(areFriends = False)
          message = foreign_data["displayName"], "unfollowed", author_data["displayName"], "and they are no longer friends"
      
        Following.objects.filter(authorid = authorid, followingid = foreignid).delete()    
  
        return JsonResponse({"message": message,"success": True})
      



@api_view(['POST'])  
def create_follow_request(request, foreignid):
    '''LOCAL
      Use this endpoint to send a follow request to an author's inbox 
      Sent to inbox of "object"'''
    
    if request.method == 'POST':
      
      if request.session.session_key is not None:
          session = Session.objects.get(session_key=request.session.session_key)
          if session:
              session_data = session.get_decoded()
              uid = session_data.get('_auth_user_id')
              user = Author.objects.get(id=uid)
    
      send_external = None

      if  Author.objects.filter(id = foreignid).exists(): # if the foreign author is saved on our server:
          foreign_author = Author.objects.get(id = foreignid)
        
      # else:
      #     split_id = foreignid.split("authors")
      #     node = Node.objects.get(baseUrl = split_id[0]) # get the host from the id
      #     username = node["theirUsername"]
      #     password = node["theirPassword"]
      #     response = requests.get(foreignid, auth=(username, password)) # send get request to node to retrieve external author info
      #     foreign_data = response.json()  
      #     send_external = "foreign"

      if Following.objects.filter(authorid = user, followingid = foreign_author).exists():
          
        return JsonResponse({"message": "You are already following this author"}, status=405)

      elif FollowRequest.objects.filter(requester = user, receiver = foreign_author).exists():
        message = user.displayName, "has already sent a follow request to", foreign_author.displayName
        
        return JsonResponse({"message": message, "success": False}, status=405)
      
      elif not FollowRequest.objects.filter(requester = user.id, receiver = foreignid).exists():
          
        # data = {
        #     "type": "Follow",      
        #     "summary": user.displayName + " wants to follow " + foreign_author.displayName,
        #     "actor":{ 
        #               "type": "author",
        #               "id": user.id,
        #               "url": user.url,
        #               "host": user.host,
        #               "displayName": user.displayName,
        #               "github": user.github,
        #               "profileImage": user.profileImage},
                    
        #     "object":{
        #               "type": "author",
        #               "id": foreign_data["id"],
        #               "url": foreign_data["url"],
        #               "host": foreign_data["host"],
        #               "displayName": foreign_data["displayName"],
        #               "github": foreign_data["github"],
        #               "profileImage": foreign_data["profileImage"]
                    
        #     }
        # }

        # if send_external == None: # if the follow request's receiver is on local server
        #     requests.post(foreign_data["host"] +"/"+ foreignid + "/inbox/", data) # data sent to local author's inbox
        FollowRequest.objects.create(requester = user.id, receiver = Author.objects.get(id = foreignid))
        
        # elif send_external == "foreign":
        #   response = requests.post(foreignid +"/inbox", data, auth=(username, password)) # data sent to foreign author's inbox
        #   if response.status != 200:
        #      return JsonResponse({"message": "Could not sent request to external node", "success": False}, status=response.status)
        
        message = user.displayName, "sent a follow request to", foreign_author.displayName
          
        return JsonResponse({"message": message, "success": True})



@api_view(['PUT']) 
def respond_to_follow_request(request, foreignid):
    ''' LOCAL 
        Respond to a follow request from another author'''
    
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

          if Following.objects.filter(authorid = user, followingid = foreign_author).exists():
            Following.objects.filter(authorid = user, followingid = foreign_author).update(areFriends = True)
            Following.objects.create(authorid = foreign_author, followingid = user, areFriends = True)
          else:
            Following.objects.create(authorid = foreign_author, followingid = user, areFriends = False)
          message = "Follow request accepted"
          #foreign_author_follow(request, authorid, foreignid)
      
        elif data["decision"] == "decline":
          FollowRequest.objects.filter(requester = foreignid, receiver = user.id).delete()
          message = "Follow request declined"
        return JsonResponse({"message": message,"success": True})
        
    return JsonResponse({"message": "Error responding to follow request",})


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
  



def check_follow_status(request):
  '''Check the follow status between two authors'''

  
  data = request.GET
  authorid = data["id"]
  print("AUTHORID:", authorid)
  author = Author.objects.get(id=authorid)

  result = {}

  if request.method == "GET":
    # follow
    if Following.objects.filter(authorid = request.user, followingid = author).exists():
      if Following.objects.filter(authorid = request.user, followingid = author)[0].areFriends:
        result["status"] = "friend"
      else:
        result["status"] = "follower"
    
    # follow pending
    elif FollowRequest.objects.filter(requester = request.user, receiver = author ).exists():
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



def get_follow_requests(request):
    '''Get all follow requests for an author'''
    
    if request.method == "GET":
      authorid = request.GET.get("id")
      if authorid:

        author = Author.objects.get(id=authorid)
        print("Here, id:", authorid)
        print("author is:", author)
        follow_requests = FollowRequest.objects.filter(receiver=author)
        requesters = []
        
        for follow_request in follow_requests:
          
          # include logic here that checks if requester has an external host
          requester = Author.objects.get(id=follow_request.requester)
          print("FOLLOW REQUESTER ID:", requester.id)
          requesters.append(requester)

        print("requesters:", requesters)
        res = serializers.serialize("json", requesters, fields=["profileImage", "username", "github", "displayName", "url"])
    
        print("res:", res)
        
        return HttpResponse(res, content_type="application/json")
      return JsonResponse({"message": "No new requests"})
    


def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})

def front_end(request, authorid):
    return render(request, 'index.html')

def get_image(request, image_file):
    return redirect(f'/images/{image_file}')


def unfollow(request):
  '''Unfollow another author'''
  unfollowedAuthor = Author.objects.get(id=authorid)

  if request.method == "POST":
      if Following.objects.filter(authorid = request.user, followingid = unfollowedAuthor).exists():
        message = unfollowedAuthor.username, "unfollowed", request.user.username

        if Following.objects.filter(authorid = request.user, followingid = unfollowedAuthor)[0].areFriends:
          Following.objects.filter(authorid = unfollowedAuthor, followingid = request.user).update(areFriends = False)
          message = unfollowedAuthor.username, "unfollowed", request.user.username, "and they are no longer friends"
        
        Following.objects.filter(authorid = request.user, followingid = unfollowedAuthor).delete()
        print(message)
        return JsonResponse({"message": message,
                              "success": True})