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
from django.contrib.auth import get_user_model

def register(request):
    '''Handles a form submission POST request to register
       returns: JSON data including success status + errors if applicable'''  
    if request.method == 'POST':  
        data ={}
        print(request.POST)
        form = Register(request.POST)
        
        if form.is_valid():  
            user = form.save()
            
            login(request, user)
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

    return render(request, "dist/index.html")
    
def loginview(request):
    '''Handles a form submission POST request to login
       returns: JSON data including success status + errors if applicable'''  
    

    if request.method == 'POST':
        
        data ={}
        user = Login.post(request)

        if user:
            login(request, user)
            data['success'] = True  
            return JsonResponse(data)  
        else:
            data['success'] = False
            return JsonResponse(data)  
        
    return render(request, 'dist/index.html')

def index(request):
    return render(request, "dist/index.html")

def is_authenticated(request):
    data = {}
    if request.user.is_authenticated:
        data['success'] = True
    else:
        data['success'] = False
    return JsonResponse(data)


