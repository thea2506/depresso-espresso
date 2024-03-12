from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from posts.models import Post
from authentication.models import Author, Following, FollowRequest

# Potentially edit this to only use 1 function
def get_profile(request, authorid):
    if request.method == "GET":
        author = get_object_or_404(Author, pk=authorid)
        data = {
            "type": "author",
            "id": author.id,
            "host": author.host,
            "displayName": author.displayName,
            "username": author.username,
            "url": author.url,
            "github": author.github,
            "profileImage": author.profileImage
        }
        return JsonResponse(data)

def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})
  
def get_authors(request):
  if request.method == "GET":
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
  else:
    return JsonResponse({"message": "Method not allowed"}, status=405)

def front_end(request, authorid):
    return render(request, 'index.html')

def get_image(request, image_file):
    return redirect(f'/images/{image_file}')

def edit_profile(request, authorid):
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
        
    return JsonResponse({"message": "Profile not updated"})

def send_follow_request(request, authorid):
    '''Send a follow request to another author'''
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

def respond_to_follow_request(request):
    '''Respond to a follow request from another author'''
    data = request.POST
    username = data["username"]
    requestingAuthor = Author.objects.get(username=username)
    print(requestingAuthor)
    if request.method == "POST":
        if data["decision"] == "accept":
          FollowRequest.objects.filter(requester = requestingAuthor, receiver = request.user).delete()
          
          if Following.objects.filter(authorid = request.user, followingid = requestingAuthor).exists():
            Following.objects.filter(authorid = request.user, followingid = requestingAuthor).update(areFriends = True)
            Following.objects.create(authorid = requestingAuthor, followingid = request.user, areFriends = True)
            message = "Follow request from", requestingAuthor.username, "accepted by", request.user.username, "and they are now friends"

          else:
            Following.objects.create(authorid = requestingAuthor, followingid = request.user, areFriends = False)
            message = "Follow request from", requestingAuthor.username, "accepted by", request.user.username
            
          print(message)
          return JsonResponse({"message": message,
                               "success": True})
        
        elif data["decision"] == "decline":
          FollowRequest.objects.filter(requester = requestingAuthor, receiver = request.user).delete()

          message = "Follow request from", requestingAuthor.username, "declined by", request.user.username
          print(message)
          return JsonResponse({"message": message,
                               "success": True})
        
    return JsonResponse({"message": "Error responding to follow request",})

def get_followers(request, authorid):
  '''Get all followers of an author'''
  if request.method == "GET":
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
  
def unfollow(request, authorid):
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