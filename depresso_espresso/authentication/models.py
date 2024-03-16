from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class Author(AbstractUser):
    type = models.CharField(max_length=50, default="author")
    id = models.UUIDField(db_column='authorID', primary_key=True, default=uuid.uuid4)
    #uuid = models.UUIDField(unique = True, db_column='authorID', primary_key= True, default=uuid.uuid4)
    host = models.URLField(null = True, blank = True)
    displayName = models.CharField(null=False, blank=False, max_length=50)
    url = models.URLField(null = True, blank = True)
    github = models.URLField(null = True, blank = True)
    profileImage = models.URLField(null = True, blank = True)

    username = models.CharField(unique=True, null=False, blank=False, max_length=50)
    allowRegister = models.BooleanField(null = False, blank = False, default=False)

class RegisterConfig(models.Model):
    requireRegisterPerms = models.BooleanField(null = False, blank = False)

class Node(models.Model):
    ourUsername = models.CharField(max_length=50) # username for their node to authenticate with ours 
    ourPassword = models.CharField(max_length=50) # password for their node to authenticate with ours 
    theirUsername = models.CharField(max_length=50) # username for our node to authenticate with theirs
    theirPassword = models.CharField(max_length=50) # password for our node to authenticate with theirs
    baseUrl = models.URLField()

    def __str__(self): # Reference: https://stackoverflow.com/questions/9336463/django-xxxxxx-object-display-customization-in-admin-action-sidebar
        return self.baseUrl

class Following(models.Model):
    authorid = models.CharField(max_length=200)
    followingid = models.CharField(max_length=200)
    areFriends = models.BooleanField(null = False, blank = False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        unique_together = ('authorid', 'followingid')
        
class FollowRequest(models.Model):
    # Assuming receivers will only ever be stored on our server but requesters can come from external authors
    requester = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)

    class Meta:
        managed = True


