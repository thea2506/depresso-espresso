from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Author(AbstractUser):
    type = models.CharField(max_length=50, default="author")
    id = models.UUIDField(db_column='authorID', primary_key=True, default=uuid.uuid4)
    host = models.URLField(null = True, blank = True)
    displayName = models.CharField(null=False, blank=False, max_length=50)
    username = models.CharField(unique=True, null=False, blank=False, max_length=50)
    url = models.URLField(null = True, blank = True)
    github = models.URLField(null = True, blank = True)
    profileImage = models.URLField(null = True, blank = True)
    allowRegister = models.BooleanField(null = False, blank = False, default=False)

class RegisterConfig(models.Model):
    requireRegisterPerms = models.BooleanField(null = False, blank = False)

class Following(models.Model):
    authorid = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="following")
    followingid = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="followers")
    areFriends = models.BooleanField(null = False, blank = False, default=False)

    class Meta:
        managed = True
        unique_together = ('authorid', 'followingid')
        
class FollowRequest(models.Model):
    requester = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="follow_requests_sent")
    receiver = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="follow_requests_received")

    class Meta:
        managed = True
