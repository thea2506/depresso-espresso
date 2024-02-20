from django.db import models
from authentication.models import Author


# Create your models here.
#---------------------------------------------------------
# Example
# Table room
# class Room(models.Model):
#     # foreign keys
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

#     name = models.CharField(max_length=200)
#     description = models.TextField(null = True, blank = True)
#     # participants = 
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         # the minus is for descending order
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return str(self.name)
#---------------------------------------------------------
# Add your table right here then run django-admin makemigrations (creates the newly added models) and django-admin migrate (add the models to the database). This process has to be done every time you add one or more models to the database.

# Add your table right here then run django-admin makemigrations (creates the newly added models) and django-admin migrate (add the models to the database).
# This process has to be done every time you add one or more models to the database.
#---------------------------------------------------------
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# Reference:
# https://www.youtube.com/watch?v=8jyyuBaZwVU




'''
Commented out because using the django AbstractUser
class Author(models.Model):
    type = models.TextField()
    authorid = models.TextField(db_column='authorID', primary_key=True)  # Field name made lowercase.
    url = models.TextField()
    host = models.TextField()
    displayname = models.TextField(db_column='displayName')  # Field name made lowercase.
    github = models.TextField(blank=True, null=True)
    profileimage = models.TextField(db_column='profileImage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'author'
'''
class Comments(models.Model):
    postid = models.ForeignKey('Posts', models.DO_NOTHING, db_column='postID')  # Field name made lowercase.
    commentid = models.TextField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    contenttype = models.TextField(db_column='contentType')  # Field name made lowercase.
    content = models.TextField()
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='authorID')  # Field name made lowercase.
    comment = models.TextField()
    publishdate = models.DateTimeField(db_column='publishDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comments'


class Following(models.Model):
    authorid = models.TextField(db_column='authorID', primary_key=True)  # Field name made lowercase. The composite primary key (authorID, followerID) found, that is not supported. The first column is selected.
    followerid = models.TextField(db_column='followerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'following'
        unique_together = (('authorid', 'followerid'),)


class Likes(models.Model):
    postid = models.ForeignKey('Posts', models.DO_NOTHING, db_column='postID')  # Field name made lowercase.
    authorid = models.OneToOneField(Author, models.DO_NOTHING, db_column='authorID', primary_key=True)  # Field name made lowercase. The composite primary key (authorID, postID) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'likes'
        unique_together = (('authorid', 'postid'),)


class Posts(models.Model):
    title = models.TextField()
    postid = models.TextField(db_column='postID', primary_key=True)  # Field name made lowercase.
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    contenttype = models.TextField(db_column='contentType')  # Field name made lowercase.
    content = models.TextField()
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='authorID')  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='commentCount', blank=True, null=True)  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='publishDate')  # Field name made lowercase.
    visibility = models.TextField()

    class Meta:
        managed = False
        db_table = 'posts'
