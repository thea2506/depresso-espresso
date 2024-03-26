from django.db import models
from authentication.models import Author
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class NotificationItem(models.Model):
    """
    A notification item is polymorphic (like, post, comments, share, follow)
    This models tracks different items that go through an author inbox
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_url = models.URLField()  # For storing the url of the foreign object

    def save(self, *args, **kwargs):
        if self.content_object and self.object_url:
            raise ValueError("Cannot have both content_object and object_url")
        super(NotificationItem, self).save(*args, **kwargs)


class Notification(models.Model):
    """
    The Notification model is an author's inbox.
    An author can receive different types of items: post, follow, like, comment, share
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.ManyToManyField(NotificationItem)
