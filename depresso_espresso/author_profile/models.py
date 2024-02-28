from django.db import models

# Create your models here.
class Author(models.Model):
    display_name = models.CharField(max_length=100)
    id=models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    github_link = models.CharField(max_length=100)
    profile_image = models.CharField(max_length=100)