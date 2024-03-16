from django.db import models
import uuid
from authentication.models import Author

# Create your models here.
class Post(models.Model):
    type = models.CharField(max_length=50, default="post")
    title = models.TextField(null = True)
    id = models.UUIDField(db_column='postID', primary_key=True, default=uuid.uuid4)

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
    likecount = models.IntegerField(db_column='likeCount', blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'comments'

class LikePost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="post_liking_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    class Meta:
        managed = True
        unique_together = ("post", "author")

class LikeComment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comment_liking_author")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comment")

    class Meta:
        managed = True
        unique_together = ("comment", "author")

class Share(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="sharing_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shared_post")

    class Meta:
        managed = True
        unique_together = ("post", "author")
