
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from rest_framework import permissions

# https://www.youtube.com/watch?v=lHYzmlx2Vso&list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb&index=7 Django Tutorial - User Registration & Sign Up Page #7 by Python Lessons
# https://www.youtube.com/watch?v=_tHabkMKh98 Django Tutorial - Creating Custom User model in Django website #4 by Python Lessons
# https://www.javatpoint.com/django-usercreationform 

class Register(UserCreationForm):
    permission_classes = (permissions.AllowAny)
    class Meta:
        model = get_user_model()
        
        fields = ("displayName", "password1", "password2")

    def save(self, host, commit=True):
        user = super(Register, self).save(commit=False)

        user.username = self.cleaned_data["displayName"]
        user.displayName = self.cleaned_data["displayName"]
        user.host = f"http://{host}/"
        user.set_password(self.cleaned_data["password1"])
        user.url = f"http://{host}/author/{user.id}"
        
        if commit:
            user.save()
        return user


