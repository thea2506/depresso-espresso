from django.db import models
from authentication.models import Author

# Create your models here.
class Notification(models.Model):
    type = models.CharField(max_length=50)
    sender_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    receiver_id = models.CharField(max_length=200, null=True)
    post_id = models.CharField(max_length=200, null=True)

