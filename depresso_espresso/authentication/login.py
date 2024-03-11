from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.contrib.auth import authenticate

class Login(LoginView):
    permission_classes = (permissions.AllowAny)
    template_name = "login.html"
    redirect_authenticated_user = True
    
    class Meta:
        model = get_user_model()
        fields = ("username", "password" )

    def post(request):
        username = request.POST["username"]
        password = request.POST["password"]

        #if (.values())["require_register_perms"] == True
        user = authenticate(request, username=username, password=password)
        return user