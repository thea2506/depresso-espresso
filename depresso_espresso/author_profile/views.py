from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from posts.models import Post
from authentication.models import Author
import json

# Potentially edit this to only use 1 function

@login_required
def profile(request):
    return render(request, "dist/index.html")
    
#@login_required
def user_data(request):
    if request.method == "GET":

        data = {}
        user = request.user
        if user:
            authorid = getattr(user, 'authorid')
            
            data['display_name'] = getattr(user, 'display_name')
            data["authorid"] = authorid
            data["host"] = f"http://{request.get_host()}/"
            data["authorurl"] = f"http://{request.get_host()}/authors/{authorid}"
            print(data["authorid"], data["host"], data["authorurl"])

            data['github_link'] = getattr(user, 'github_link')
            data['profile_image'] = getattr(user, 'profile_image')
            data['username'] = getattr(user, 'username')
            data['success'] = True
            #data['follows'] = getattr(user, 'follows')
            #data['friends'] = getattr(user, 'friends')
            friends = getattr(user, 'friends')
            print("username:", getattr(user, 'username'))
            print("FRIENDS:", friends)
            #data['username'] = getattr(user, 'username') May want to display this as well as display name 

        else:
            data['success'] = False
    
        return JsonResponse(data)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            author = get_object_or_404(Author, pk=user.authorid)
            author.display_name = data.get('displayName', author.display_name)
            author.github_link = data.get('github', author.github_link)
            author.profile_image = data.get('profileImage', author.profile_image)
            author.save()
            return JsonResponse({"message": "Profile updated successfully!"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    elif request.method == "POST":

        user = request.user
        if user:
            if "display_name" in request.POST:
                setattr(user, 'display_name', request.POST["display_name"])
            if "github_link" in request.POST:
                setattr(user, 'github_link', request.POST["github_link"])
            if "profile_image" in request.POST:
                setattr(user, 'profile_image', request.POST["profile_image"])
            user.save()

        return JsonResponse({"message": "Profile updated successfully!"})

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

def user_posts(request, username):
    user_posts = Post.objects.filter(authorid__username=username)
    return render(request, 'author_profile/user_posts.html', {'user_posts': user_posts})

# #         Single Author
# # URL: ://service/authors/{AUTHOR_ID}/
# # GET [local, remote]: retrieve AUTHOR_ID's profile
# # PUT [local]: update AUTHOR_ID's profile
# # Example Format:
# # {
# #     "type":"author",
# #     // ID of the Author
# #     "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
# #     // the home host of the author
# #     "host":"http://127.0.0.1:5454/",
# #     // the display name of the author
# #     "displayName":"Lara Croft",
# #     // url to the authors profile
# #     "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
# #     // HATEOS url for Github API
# #     "github": "http://github.com/laracroft",
# #     // Image from a public domain
# #     "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
# # }