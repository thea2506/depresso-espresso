from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
            data['display_name'] = getattr(user, 'display_name')
            data['github_link'] = getattr(user, 'github_link')
            data['profile_image'] = getattr(user, 'profile_image')
            #data['follows'] = getattr(user, 'follows')
            #data['friends'] = getattr(user, 'friends')
            #data['username'] = getattr(user, 'username') May want to display this as well as display name 
        return JsonResponse(data)
