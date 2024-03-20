from django.db import models
from authentication.models import Author
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class NotificationItem(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)

    # For local data, storing an object
    content_object = GenericForeignKey('content_type', 'object_id')

    # For remote data, storing a json field
    json_data = models.JSONField(null=True, blank=True)


class Notification(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.ManyToManyField(NotificationItem)
