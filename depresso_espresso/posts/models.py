from django.db import models
import uuid
from authentication.models import Author

# Create your models here.
class Post(models.Model):
    type = models.CharField(max_length=50, default="post")
    title = models.TextField(null = True)
    url = models.CharField(db_column='postID', primary_key=True, max_length=200)
    id = models.UUIDField(db_column='postUUID', primary_key=True, default=uuid.uuid4)

    # Origins
    source = models.TextField(blank=True, null = True)
    origin = models.TextField(blank=True, null = True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorID')
    
    # Content
    description = models.TextField(null = True)
    contentType = models.TextField(db_column='contentType', null = True)
    content = models.TextField(db_column='content', null = True)

    # Interactions tracking
    count = models.IntegerField(db_column='commentCount', blank=True, null=True, default=0)
    likecount = models.IntegerField(db_column='likeCount', blank=True, null=True, default=0)
    sharecount = models.IntegerField(db_column='sharecount', blank=True, null=True, default=0)
    comments = models.URLField(blank=True, null=True) # URL to first page of comments

    published = models.DateTimeField(db_column='publishDate', null = True, blank=True)
    
    # Visibility is one of ["PUBLIC", "FRIENDS", "UNLISTED"]
    visibility = models.TextField(null = True)

    class Meta:
        managed = True

class Comment(models.Model):
    # postid is still a post object and not postid
    # current name is just to account for django's oppressive naming convention
    postid = models.ForeignKey(Post, on_delete=models.CASCADE) 
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    id = models.UUIDField(db_column='commentID', primary_key=True, default=uuid.uuid4) # Maybe make read-only?

    contenttype = models.TextField(db_column='contentType', null = True, blank=True)
    comment = models.TextField()

    publishdate = models.DateTimeField(db_column='publishDate')

    # Visibility is one of ["PUBLIC", "FRIENDS", "UNLISTED"]
    visibility = models.TextField(null = True)

    class Meta:
        managed = True
        db_table = 'comments'

class Like(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="liking_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    class Meta:
        managed = True
        unique_together = ("post", "author")

class Share(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="sharing_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shared_post")

    class Meta:
        managed = True
        unique_together = ("post", "author")
