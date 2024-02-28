from django.db import models
import uuid
from authentication.models import Author

# Create your models here.
class Post(models.Model):
    authorid = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorID')
    postid = models.UUIDField(db_column='postID', primary_key=True, default=uuid.uuid4) # Maybe make read-only?
    authorname = models.TextField(null = True)

    title = models.TextField(null = True)
    source = models.TextField(null = True)
    origin = models.TextField(null = True)
    description = models.TextField(null = True)
    contenttype = models.TextField(db_column='contentType')
    content = models.TextField(null = True)

    image_url = models.URLField(blank=True, null=True)
    linked_img_post = models.TextField("self", blank = True, null = True)
    
    publishdate = models.DateTimeField(db_column='publishDate')
    editdate = models.DateTimeField(db_column='editDate', null = True, blank=True)

    visibility = models.TextField(null = True)
    commentcount = models.IntegerField(db_column='commentCount', blank=True, null=True)
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
