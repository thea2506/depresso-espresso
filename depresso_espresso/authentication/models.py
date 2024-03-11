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
    follows = models.ManyToManyField("self", blank=True)
    followRequests = models.ManyToManyField("self", symmetrical=False, related_name='pending_follow_requests', blank=True)
    friends = models.ManyToManyField("self", blank=True)
    allowRegister = models.BooleanField(null = False, blank = False, default=False)

class RegisterConfig(models.Model):
    requireRegisterPerms = models.BooleanField(null = False, blank = False)
