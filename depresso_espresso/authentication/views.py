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
from django.contrib.sessions.models import Session
from authentication.models import Author
from django.core import serializers
from .models import RegisterConfig
from rest_framework.decorators import api_view



def register(request):
    ''' LOCAL ONLY
        Handles a form submission POST request to register
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
                errors.append(error)  

            data['errors'] = errors   
            data['success'] = False
            return JsonResponse(data)  
    else:
        form = Register()

    return render(request, "index.html")
    
def loginUser(request):
    ''' LOCAL ONLY
        Handles a form submission POST request to login
        returns: JSON data including success status + errors if applicable'''
    if request.method == 'POST':
        user = Login.post(request)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request, "index.html")

def logoutUser(request):
    ''' LOCAL ONLY
        Handles a form submission POST request to login
        returns: JSON data including success status '''
    
    data = {}
    logout(request)
    if request.user.is_authenticated:
        data['success'] = False
    else:
        data['success'] = True
    return JsonResponse(data)

def curUser(request):
    '''LOCAL ONLY '''
    data = {} 
    if request.method == 'GET' and request.session.session_key is not None:
        session = Session.objects.get(session_key=request.session.session_key)
        if session:
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            user = Author.objects.get(id=uid)

            data["type"] = user.type
            data["id"] = user.id
            data["username"] = user.username
            data["displayName"] = user.displayName
            data["host"] = user.host
            data["url"] = user.url
            data["github"] = user.github
            data["profileImage"] = user.profileImage
            data["success"] = True
        return JsonResponse(data)
    return JsonResponse({'success': False})



