from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from posts.models import Post
from authentication.models import Author

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
    author = Author.objects.get(id=authorid)
    print(request.user, author, request.user == author)
    if request.method == "POST":
        data = request.POST
        if request.user == author:
          author.displayName = data['displayName']
          author.github = data['github']
          author.profileImage = data['profileImage']
          author.save()
          return JsonResponse({"message": "Profile updated successfully"})
        else:
          return send_follow_request(request, authorid)
        
    return JsonResponse({"message": "Profile not updated"})

def send_follow_request(request, authorid):
    requestedAuthor = Author.objects.get(id=authorid)
    print(request.user, "is sending a follow request to", requestedAuthor)
    if request.method == "POST":
        if request.user not in requestedAuthor.followRequests.all():
          requestedAuthor.followRequests.add(request.user)
          
          return JsonResponse({"message": "Follow request sent"})
        
    return JsonResponse({"message": "Follow request not sent"})

def respond_to_follow_request(request):
    data = request.POST
    username = data["username"]
    print(username)
    requestedAuthor = Author.objects.get(username=username)
    print(request.user, "is sending a follow request to", requestedAuthor)
    if request.method == "POST":
        if data["decision"] == "accept":
          
          print("Follow request from", requestedAuthor, "accepted by", request.user)
          return JsonResponse({"message": "Follow request accepted",
                               "success": True})
        
        elif data["decision"] == "declined":
          
          print("Follow request from", requestedAuthor, "declined by", request.user)
          return JsonResponse({"message": "Follow request declined",
                               "success": True})
        
    return JsonResponse({"message": "Follow request not sent"})