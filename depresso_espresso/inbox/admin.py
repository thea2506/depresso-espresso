from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationModel(admin.ModelAdmin):
    fields = ("author", "type")

admin.site.register(Notification, NotificationModel)