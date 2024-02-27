from .models import Post
from .models import Comment
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.

class PostCreationForm(forms.ModelForm):
    """A form for creating new posts."""
    class Meta:
        model = Post
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
        model = Post
        fields = ('content', 'image_url', 'publishdate', 'authorid')

class PostsAdmin(admin.ModelAdmin):
    list_display = ('content', 'image_url', 'publishdate', 'authorid', 'postid')

class CommentCreationForm(forms.ModelForm):
    """A form for creating new comments."""
    class Meta:
        model = Comment
        fields = ('postid', 'authorid', 'publishdate', 'comment')

    def save(self, commit=True):
        # Save the provided password in hashed format
        comment = super().save(commit=False)

        if commit:
            comment.save()
        return comment

class CommentChangeForm(forms.ModelForm):
    """A form for updating comments"""

    class Meta:
        model = Comment
        fields = ('postid', 'authorid', 'publishdate', 'comment')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('postid', 'authorid', 'publishdate', 'comment', "commentid")

admin.site.register(Post, PostsAdmin)
admin.site.register(Comment, CommentsAdmin)