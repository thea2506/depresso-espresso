from .models import Posts
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.

class PostCreationForm(forms.ModelForm):
    """A form for creating new posts."""
    class Meta:
        model = Posts
        fields = ('content', 'image_url', 'publishdate', 'authorid')

    def save(self, commit=True):
        # Save the provided password in hashed format
        post = super().save(commit=False)

        if commit:
            post.save()
        return post

class PostChangeForm(forms.ModelForm):
    """A form for updating posts"""

    class Meta:
        model = Posts
        fields = ('content', 'image_url', 'publishdate', 'authorid')



class PostsAdmin(admin.ModelAdmin):
    list_display = ('content', 'image_url', 'publishdate', 'authorid', 'postid')


admin.site.register(Posts, PostsAdmin)
