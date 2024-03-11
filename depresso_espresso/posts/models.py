from django.db import models
import uuid
from authentication.models import Author

# Create your models here.
class Post(models.Model):
    type = models.CharField(max_length=50, default="post")
    title = models.TextField(null = True)
    id = models.UUIDField(db_column='postID', primary_key=True, default=uuid.uuid4)
    published = models.DateTimeField(db_column='editDate', null = True, blank=True)
    
    # visibility ["PUBLIC","FRIENDS","UNLISTED"]
    visibility = models.TextField(null = True)
    
    # Origins
    source = models.TextField(null = True)
    origin = models.TextField(null = True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorID')
    
    # Content
    description = models.TextField(null = True) 
    contentType = models.TextField(db_column='contentType', null = True)
    content = models.TextField(db_column='content', null = True)

    # Interactions tracking
    count = models.IntegerField(db_column='commentCount', blank=True, null=True, default=0)
    comments = models.URLField() # URL to first page of comments
    liked_by = models.ManyToManyField(Author, related_name='liked_posts')

    class Meta:
        managed = True

class Comment(models.Model):
    postid = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='postID') 
    commentid = models.UUIDField(db_column='commentID', primary_key=True, default=uuid.uuid4) # Maybe make read-only?
    authorid = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorID')
    authorname = models.TextField(null = True)

    contenttype = models.TextField(db_column='contentType', null = True, blank=True)
    comment = models.TextField()
    publishdate = models.DateTimeField(db_column='publishDate')
    editdate = models.DateTimeField(db_column='editDate', null = True, blank=True)

    commentlikecount = models.IntegerField(db_column='commentLikeCount', blank=True, null=True)
    liked_by = models.ManyToManyField(Author, related_name='liked_comments')

    class Meta:
        managed = True
        db_table = 'comments'
