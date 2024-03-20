from django.contrib import admin
from .models import Notification, NotificationItem
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django import forms


# Register your models here.


class NotificationInline(GenericInlineModelAdmin):
    model = NotificationItem


class NotificationModel(admin.ModelAdmin):
    inlines = [NotificationInline]


class NotificationChangeForm(forms.ModelForm):
    """A form for updating notification"""

    class Meta:
        model = Notification
        fields = ('author', 'items')


admin.site.register(Notification)
admin.site.register(NotificationItem)
