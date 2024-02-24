from django.contrib import admin
from .models import Posts

# Register your models here.



class PostsAdmin(admin.ModelAdmin):
    fields = ["postid", "authorid", "content", "image_url"]


admin.site.register(Posts, PostsAdmin)
