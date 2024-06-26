from .models import Post, Comment, Share, LikePost, LikeComment
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.


class PostCreationForm(forms.ModelForm):
    """A form for creating new posts."""
    class Meta:
        model = Post
        fields = ('content', 'author', 'contenttype', 'description',
                  'title', 'source', 'origin', 'visibility', 'count', )

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
        fields = ('content', 'author', 'contenttype', 'description',
                  'title', 'source', 'origin', 'visibility', 'count', )


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'published', 'content', 'contenttype',
                    'visibility', 'count', 'likecount', 'sharecount', )


class CommentCreationForm(forms.ModelForm):
    """A form for creating new comments."""
    class Meta:
        model = Comment
        fields = ('post', 'author', 'comment',
                  'contenttype',)

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
        fields = ('comment',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'published', 'comment', "id")


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'author', 'post', "comment")


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')


admin.site.register(Post, PostsAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(LikePost)
admin.site.register(LikeComment)
