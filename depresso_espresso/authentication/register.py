from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7 Django Tutorial - User Registration & Sign Up Page #7 by Python Lessons
# https://www.youtube.com/watch?v=_tHabkMKh98 Django Tutorial - Creating Custom User model in Django website #4 by Python Lessons
# https://www.javatpoint.com/django-usercreationform 

class Register(UserCreationForm):
    github_link = forms.URLField(label = "github URL", required = False)
    profile_image = forms.URLField(label = "profile picture", required= False)
    #template_name = "register.html",

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "password", "github_link", "profile_image")
