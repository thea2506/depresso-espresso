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
      authors = Author.objects.filter(display_name__icontains=search_terms)
    else:
      authors = Author.objects.all()
    
    data = []
    for author in authors:
      data.append({
        "type": "author",
        "id": f"http://{request.get_host()}/authors/{author.pk}",
        "url": f"http://{request.get_host()}/authors/{author.pk}",
        "host": f"http://{request.get_host()}/",
        "displayName": author.display_name,
        "username": author.username,
        "github": author.github_link,
        "profileImage": author.profile_image
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

    if request.method == "POST":
        data = request.POST
        if request.user == author:
          author.displayName = data['displayName']
          author.github = data['github']
          author.profileImage = data['profileImage']
          author.save()
          return JsonResponse({"message": "Profile updated successfully"})
        
    return JsonResponse({"message": "Profile not updated"})