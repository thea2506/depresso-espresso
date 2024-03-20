from django.db import models
import uuid
from authentication.models import Author


class Post(models.Model):

    # Identifiers
    id = models.UUIDField(db_column='postID',
                          primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, db_column='authorID')
    source = models.TextField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    published = models.DateTimeField(
        db_column='published', null=True, blank=True)

    # Visibility is one of ["PUBLIC", "FRIENDS", "UNLISTED"]
    visibility = models.TextField(null=True)

    # Content
    type = models.CharField(max_length=50, default="post", editable=False)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    contentType = models.TextField(db_column='contentType', null=True)
    content = models.TextField(db_column='content', null=True)

    # Interactions tracking
    count = models.IntegerField(
        db_column='commentCount', blank=True, null=True, default=0)  # Comment count
    likecount = models.IntegerField(
        db_column='likeCount', blank=True, null=True, default=0)
    sharecount = models.IntegerField(
        db_column='sharecount', blank=True, null=True, default=0)
    # URL to first page of comments
    comments = models.URLField(blank=True, null=True)

    class Meta:
        managed = True


class Comment(models.Model):

    # Identiiers

    # postid is still a post object and not a string/uuid
    # current name is just to account for django's oppressive naming convention
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    id = models.UUIDField(db_column='commentID',
                          primary_key=True, default=uuid.uuid4)
    published = models.DateTimeField(db_column='published', auto_now_add=True)

    # Visibility is one of ["PUBLIC", "FRIENDS", "UNLISTED"]
    visibility = models.TextField(null=True)

    # Content/interactions
    contentType = models.TextField(
        db_column='contentType', null=True, blank=True)
    comment = models.TextField()
    likecount = models.IntegerField(
        db_column='likeCount', blank=True, null=True, default=0)

    type = models.CharField(max_length=50, default="comment", editable=False)

    class Meta:
        managed = True
        db_table = 'comments'


class Share(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="sharing_author")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="shared_post")

    class Meta:
        managed = True
        unique_together = ("post", "author")


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(default="", editable=False)
    # Author can be foreign
    author = models.JSONField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
