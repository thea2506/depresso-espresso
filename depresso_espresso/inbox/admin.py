from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationModel(admin.ModelAdmin):
    fields = ("author", "message", "is_read")

admin.site.register(Notification, NotificationModel)