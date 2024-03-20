from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Author(AbstractUser):
    id = models.UUIDField(db_column='authorID',
                          primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        unique=True, null=False, blank=False, max_length=50)
    url = models.URLField(null=True, blank=True)
    host = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=50, default="author")
    displayName = models.CharField(null=False, blank=False, max_length=50)
    github = models.URLField(null=True, blank=True)
    profileImage = models.URLField(null=True, blank=True)

    # For US.08.02. When admin changes requireRegisterPerms, this field
    # will be changed so that users need an OK to login after registering
    allowRegister = models.BooleanField(null=False, blank=False, default=False)

    # Identifier to separate local and external authors
    isExternalAuthor = models.BooleanField(
        null=False, blank=False, default=False)


class RegisterConfig(models.Model):
    requireRegisterPerms = models.BooleanField(null=False, blank=False)


class Node(models.Model):
    host = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=True)


class Following(models.Model):

    authorid = models.CharField(max_length=200)
    followingid = models.CharField(max_length=200)
    areFriends = models.BooleanField(null=False, blank=False, default=False)
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


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object = models.ForeignKey("Author", on_delete=models.CASCADE)
    actor = models.JSONField()


class Follower(models.Model):
    class Meta:
        constraints = [
            # follower_author can only follow author once
            models.UniqueConstraint(
                fields=["author", "follower_author"], name="unique_follower"),
        ]

    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    follower_author = models.JSONField()
