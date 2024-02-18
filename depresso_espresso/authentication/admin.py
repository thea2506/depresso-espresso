from django.contrib import admin
from .models import Author

# Register your models here.
# User registration: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'github_link', 'profile_image')

    # todo: https://stackoverflow.com/questions/18108521/how-to-show-a-many-to-many-field-with-list-display-in-django-admin

admin.site.register(Author, AuthorAdmin)