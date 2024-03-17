from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationModel(admin.ModelAdmin):
    fields = ("sender_id", "receiver_id", "post_id", "type")

admin.site.register(Notification, NotificationModel)