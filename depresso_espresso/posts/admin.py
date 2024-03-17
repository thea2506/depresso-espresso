from .models import Post, Comment, LikePost, LikeComment, Share
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
        fields = ('content', 'published', 'author')

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
        fields = ('content', 'published', 'author')

class PostsAdmin(admin.ModelAdmin):
    list_display = ('content', 'published', 'author', 'id')

class CommentCreationForm(forms.ModelForm):
    """A form for creating new comments."""
    class Meta:
        model = Comment
        fields = ('postid', 'author', 'publishdate', 'comment')

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
        fields = ('postid', 'author', 'publishdate', 'comment')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('postid', 'author', 'publishdate', 'comment', "id")

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')

@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment')

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')

admin.site.register(Post, PostsAdmin)
admin.site.register(Comment, CommentsAdmin)