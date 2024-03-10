# References:
# https://www.techwithtim.net/tutorials/django/user-registration 2/17/2024
# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7 2/17/2024
# https://stackoverflow.com/questions/75401759/how-to-set-up-login-view-in-python-django 2/17/2024
# https://stackoverflow.com/questions/69319964/passing-data-from-django-view-context-dictionary-to-react-components answer from Rvector 2/19/2024

from django.shortcuts import render
from .register import Register
from .login import Login
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core import serializers

def register(request):
    '''Handles a form submission POST request to register
       returns: JSON data including success status + errors if applicable'''  
    if request.method == 'POST':  
        data ={}
        form = Register(request.POST)
        
        if form.is_valid():
            form.save(request.get_host())
            data['success'] = True  
            return JsonResponse(data)  
        else:
            errors = []
            for error in list(form.errors.values()):              
                print(request, form.errors.items(), error)
                errors.append(error)  

            data['errors'] = errors   
            data['success'] = False
            return JsonResponse(data)  
    else:
        form = Register()

    return render(request, "index.html")
    
def loginUser(request):
    '''Handles a form submission POST request to login
       returns: JSON data including success status + errors if applicable'''
    if request.method == 'POST':
        user = Login.post(request)
        return JsonResponse({
            "displayName": user.displayName,
            "type": user.type,
            "url": user.url,
            "id": user.id,
            "github": user.github,
            "profileImage": user.profileImage,

            "isAuthenticated": user.is_authenticated,
            "success": user is not None,
        }) 

def frontend(request):
    return render(request, "index.html")

def logoutUser(request):
    data = {}
    logout(request)
    
    if request.user.is_authenticated:
        data['success'] = False
    else:
        data['success'] = True
    return JsonResponse(data)
