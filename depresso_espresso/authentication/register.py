from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7 Django Tutorial - User Registration & Sign Up Page #7 by Python Lessons
# https://www.youtube.com/watch?v=_tHabkMKh98 Django Tutorial - Creating Custom User model in Django website #4 by Python Lessons
# https://www.javatpoint.com/django-usercreationform 

class Register(UserCreationForm):
    #github_link = forms.URLField(label = "github URL", required = False)
    #profile_image = forms.URLField(label = "profile picture", required= False)
    #first_name= forms.CharField(label = 'first_name')
    #last_name= forms.CharField(label = 'last_name')
   # username= forms.CharField(label = 'Username')
   # password= forms.CharField(label = 'Password')
   # template_name = "register.html",
    

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "password", "github_link", "profile_image")

    def save(self, commit=True):
        user = super(Register, self).save(commit=False) # call save from parent UserCreationForm
        

        # Assign form data to user fields
        #user.first_name = self.cleaned_data('first_name')
       # user.last_name = self.cleaned_data('last_name')
        #user.github_link = self.cleaned_data('github_link')
       # user.profile_image = self.cleaned_data('profile_image')
        if commit:
            user.save()

        return user


