from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from posts.models import Post
from authentication.models import Author, Following, FollowRequest, Node
from rest_framework.decorators import api_view
from authentication.checkbasic import checkBasic
import requests



@api_view(['GET', 'PUT'])
def author_profile(request, authorid):
    ''' LOCAL and REMOTE GET ://service/authors/{AUTHOR_ID}: Returns the profile information for authorid
        LOCAL PUT ://service/authors/{AUTHOR_ID}: Updates the profile information for authorid'''
    
    if request.method == "GET":
        
        if request.user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          
        if Author.objects.filter(id = authorid).exists():
          if request.META["HTTP_HOST"] in authorid: # if the author is saved on our server:
             author = Author.objects.get(id = authorid)
             author_data = author.values()[0]
             
          else:
             response = requests.get(authorid) # send get request to node to retrieve external author info
             author_data = response.json()      
          
          data = {
             {
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
           return JsonResponse({"message:" "Author not found"}, status=404)
          
    
    if request.method == "PUT":
        if request.user.is_authenticated == True:
          author = get_object_or_404(Author, pk=authorid)
          data = request.PUT
          if request.user == author:
            if data.get('displayName') != None:
              author.displayName = data['displayName']
            if data.get('github') != None:
              author.github = data['github']
            if data.get('profileImage') != None:
              author.profileImage = data['profileImage']
            author.save()
            return JsonResponse({"message": "Profile updated successfully"})
          

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
  
  if request.method == "GET":

    if request.user.is_authenticated == False:
          node = checkBasic(request)
          if not node:
             return JsonResponse({"message:" "External Auth Failed"}, status=401)
          

    followers = Following.objects.filter(followingid=authorid)
    data = []

    for follower in followers:
      user = Author.objects.get(id=follower.authorid.id)
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
  

@api_view(['GET', 'DELETE', 'PUT'])  
def foreign_author_follow(request, authorid, foreignid):
    ''' LOCAL AND REMOTE GET ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        LOCAL PUT ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        LOCAL DELETE ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}: Unfollow another author'''
    
    if request.user.is_authenticated == False:
        node = checkBasic(request)
        if not node:
            return JsonResponse({"message:" "External Auth Failed"}, status=401)

    if request.method == "GET":
       if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          if request.META["HTTP_HOST"] in authorid: # if the author is saved on our server:
             author = Author.objects.get(id = authorid)
             author_data = author.values()[0]
             
          else:
             response = requests.get(authorid) # send get request to node to retrieve external author info
             author_data = response.json()

          if request.META["HTTP_HOST"] in foreignid: # if the foreign author is saved on our server:
             foreign_author = Author.objects.get(id = foreignid)
             foreign_data = foreign_author.values()[0]
            
          else:
             response = requests.get(foreignid) # send get request to node to retrieve external author info
             foreign_data = response.json()          
          
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
      
    if request.method == "PUT":

      if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          Following.objects.filter(authorid = foreignid, followingid = authorid).update(areFriends = True)
          Following.objects.create(authorid = authorid, followingid = foreignid, areFriends = True)
          #message = "Follow request from", requestingAuthor.username, "accepted by", request.user.username, "and they are now friends" Can deal with this message once i make sure it works
          message = "Follow request accepted. You are now friends"

      else:
        Following.objects.create(authorid = foreignid, followingid = authorid, areFriends = False)
        #message = "Follow request from", requestingAuthor.username, "accepted by", request.user.username
        message = "Follow request accepted"

      return JsonResponse({"message": message,"success": True})
       
      
    if request.method == "DELETE":        
      data = request.DELETE
      #authorid = data["authorid"]
      #foreignid = data["foreignid"]

      #unfollowedAuthor = Author.objects.get(authorid=foreignid)
      
      if Following.objects.filter(authorid = authorid, followingid = foreignid).exists():
        #message = unfollowedAuthor.username, "unfollowed", request.user.username     Simplified message because since authors can be saved on external nodes, we don't have easy access to the external author's username/ display name without sending a GET req to the foreign author's host server
        message = "You have unfollowed this author."

        if Following.objects.filter(authorid = authorid, followingid = foreignid).areFriends:
          Following.objects.filter(authorid = authorid, followingid = foreignid).update(areFriends = False)
          #message = unfollowedAuthor.username, "unfollowed", request.user.username, "and they are no longer friends"
          message = "You are no longer friends with this author."
            
          Following.objects.filter(authorid = authorid, followingid = foreignid).delete()
          return JsonResponse({"message": message,
                                "success": True})

   
def create_follow_request(request, authorid, foreignid):
   '''LOCAL
      Use this endpoint to send a follow request to an author's inbox 
      Sent to inbox of "object"'''
   
   send_external = False
   
   if Following.objects.filter(authorid = foreignid, followingid = authorid).exists():
          
      return JsonResponse({"message": "You are already following this author"}, status=405)
   
   else:

      if request.META["HTTP_HOST"] in authorid: # if the author is saved on our server:
          author = Author.objects.get(id = authorid)
          author_data = author.values()[0]
          
      else:
          node = Node.objects.get(baseUrl = request.META["HTTP_HOST"])
          username = node["thierUsername"]
          password = node["thierPassword"]
          response = requests.get(authorid) # send get request to node to retrieve external author info
          author_data = response.json()

      if request.META["HTTP_HOST"] in foreignid: # if the foreign author is saved on our server:
          foreign_author = Author.objects.get(id = foreignid)
          foreign_data = foreign_author.values()[0]
        
      else:
          response = requests.get(foreignid) # send get request to node to retrieve external author info
          foreign_data = response.json()   
                     
      
      data = {
          "type": "Follow",      
          "summary": author_data["displayName"] + " wants to follow " + foreign_data["displayName"],
          "actor":{ 
                    "type": "author",
                    "id": author_data["id"],
                    "url": author_data["url"],
                    "host": author_data["host"],
                    "displayName": author_data["displayName"],
                    "github": author_data["github"],
                    "profileImage": author_data["profileImage"]},
                  
          "object":{
                    "type": "author",
                    "id": foreign_data["id"],
                    "url": foreign_data["url"],
                    "host": foreign_data["host"],
                    "displayName": foreign_data["displayName"],
                    "github": foreign_data["github"],
                    "profileImage": foreign_data["profileImage"]
                  
          }
      }

      

      return JsonResponse(data)
  



def send_follow_request(request, authorid, foreignid):
    '''Send a follow request to another author
        GET ://service/authors/{AUTHOR_ID}/followers 
        '''
    


























    requestedAuthor = Author.objects.get(id=authorid)
    
    if request.method == "POST":
        if not FollowRequest.objects.filter(requester = request.user, receiver = requestedAuthor).exists():
          FollowRequest.objects.create(requester = request.user, receiver = requestedAuthor)

          message = request.user.username, "sent a follow request to", requestedAuthor.username
          print(message)
          
          return JsonResponse({"message": message,
                               "success": True})
        
        elif FollowRequest.objects.filter(requester = request.user, receiver = requestedAuthor).exists():
          message = request.user.username, "has already sent a follow request to", requestedAuthor.username
          print(message)
          
          return JsonResponse({"message": message,
                               "success": False})
        
    return JsonResponse({"message": "Follow request not sent",
                         "success": False})




  

def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})

def front_end(request, authorid):
    return render(request, 'index.html')

def get_image(request, image_file):
    return redirect(f'/images/{image_file}')

# edit profile has been merged with author profile as a PUT request to match requirements
""" def edit_profile(request, authorid):
    '''Edit the profile of an author'''
    author = Author.objects.get(id=authorid)
    if request.method == "POST":
        data = request.POST
        if request.user == author:
          if data.get('displayName') != None:
            author.displayName = data['displayName']
          author.github = data['github']
          author.profileImage = data['profileImage']
          author.save()
          return JsonResponse({"message": "Profile updated successfully"})
        else:
          return send_follow_request(request, authorid)
        
    return JsonResponse({"message": "Profile not updated"}) """



def respond_to_follow_request(request):
    ''' LOCAL 
        Respond to a follow request from another author'''
    
    data = request.PUT
    foreignid = data["authorid"]
    requestingAuthor = Author.objects.get(username=username)
    print(requestingAuthor)
    if request.method == "PUT":
        if data["decision"] == "accept":
          FollowRequest.objects.filter(requester = requestingAuthor, receiver = request.user).delete()
          foreign_author_follow(request, username, requestingAuthor)

          
          
          
        
        elif data["decision"] == "decline":
          FollowRequest.objects.filter(requester = requestingAuthor, receiver = request.user).delete()

          message = "Follow request from", requestingAuthor.username, "declined by", request.user.username
          print(message)
          return JsonResponse({"message": message,
                               "success": True})
        
    return JsonResponse({"message": "Error responding to follow request",})



def get_friends(request, authorid):
  '''Get all friends of an author'''
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
  
""" def unfollow(request):
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
                              "success": True}) """
      
def check_follow_status(request):
  '''Check the follow status between two authors'''
  data = request.GET
  authorid = data["id"]
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
    authorid = request.GET.get("id")
    if request.method == "GET":
      follow_requests = FollowRequest.objects.filter(receiver=authorid)
      requesters = []
      for follow_request in follow_requests:
        requester = follow_request.requester
        requesters.append(requester)
      res = serializers.serialize("json", requesters, fields=["profileImage", "username", "github", "displayName", "url"])
      return HttpResponse(res, content_type="application/json")