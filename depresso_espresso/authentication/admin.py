from django.contrib import admin
from .models import Author, RegisterConfig
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.
# User registration: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site 2/17/2024
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example 2/19/2024
# For only allowing 1 RegisterConfiguration: https://stackoverflow.com/questions/39412968/allow-only-one-instance-of-a-model-in-django answer from Ivan Semochkin 3/9/2024

class RegisterConfigForm(forms.ModelForm):
    """A form for configuring optional user registration admin perms"""
    class Meta:
        model = RegisterConfig
        fields = ('require_register_perms',)

    def save(self):
        if not self.pk and RegisterConfig.objects.exists():
            raise ValidationError("Only one RegisterConfig instance allowed")
        return super(RegisterConfig, self).save()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. From django documentation."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Author
        fields = ('username', 'first_name', 'last_name', "github_link", "profile_image", "display_name", "friends")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. From django documentation."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Author
        fields = ('username', 'first_name', 'last_name', "github_link", "profile_image", "display_name")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        return self.initial["password"]

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'github_link', 'profile_image', 'is_active', 'password', "display_name")

class RegisterConfigAdmin(admin.ModelAdmin):
    fields = ('require_register_perms',)

    # todo: https://stackoverflow.com/questions/18108521/how-to-show-a-many-to-many-field-with-list-display-in-django-admin

admin.site.register(Author, AuthorAdmin)
admin.site.register(RegisterConfig, RegisterConfigAdmin)