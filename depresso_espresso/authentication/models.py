from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Author(AbstractUser):
    github_link = models.URLField(null = True, blank = True)
    profile_image = models.URLField(null = True, blank = True)
    follows = models.ManyToManyField("self", blank=True, null=True) #https://stackoverflow.com/questions/11721157/django-many-to-many-m2m-relation-to-same-model
    friends = models.ManyToManyField("self", blank=True, null=True)