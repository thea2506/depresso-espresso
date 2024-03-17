from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.contrib.auth import authenticate
from .models import Author

from rest_framework.views import APIView

class Login(APIView, LoginView):
    permission_classes = (permissions.AllowAny)
    template_name = "login.html"
    redirect_authenticated_user = True
    
    class Meta:
        model = get_user_model()
        fields = ("username", "password" )

    def post(request):
        username = request.POST["username"]
        password = request.POST["password"]

        unauthenticated_user = Author.objects.filter(username = username)

        if len(unauthenticated_user.values()) == 1:
            if (unauthenticated_user.values())[0]["allowRegister"] == False:
                user = None # force authenticaiton failure if user is not allowed registration access yet (Could eventually show the user an error)
                return user
            
                
        user = authenticate(request, username=username, password=password) # if execution reaches this point the user does not exist in database
        return user
        