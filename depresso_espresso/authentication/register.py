from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.contrib.auth import authenticate
from .models import RegisterConfig

# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7 Django Tutorial - User Registration & Sign Up Page #7 by Python Lessons
# https://www.youtube.com/watch?v=_tHabkMKh98 Django Tutorial - Creating Custom User model in Django website #4 by Python Lessons
# https://www.javatpoint.com/django-usercreationform 

class Register(UserCreationForm):
    permission_classes = (permissions.AllowAny)
    template_name = "register.html", 

    class Meta:
        model = get_user_model()
        fields = ("display_name", "username", "password1", "password2" )

    def save(self, commit=True):
        user = super(Register, self).save(commit=False) # call save from parent UserCreationForm

        user.display_name = self.cleaned_data["display_name"]

        register_config = (RegisterConfig.objects.all())[:1]
        if len(register_config) == 0:
            register_config = RegisterConfig.objects.create(require_register_perms=False) # create new register config object that has its require_register_perms set to false by default (admin can change this setting)
        
        if (register_config.values())[0]["require_register_perms"] == False:
            user.allow_register = True
        else:
            user.allow_register = False

        
        #user = authenticate(self.cleaned_data["username"], self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


