from django.db import models
import uuid
from authentication.models import Author

# Create your models here.
class Posts(models.Model):
    title = models.TextField(null = True)
    postid = models.UUIDField(db_column='postID', primary_key=True, default=uuid.uuid4) # Maybe make read-only?
    source = models.TextField(null = True)
    origin = models.TextField(null = True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(null = True)
    contenttype = models.TextField(db_column='contentType', null = True)  # Field name made lowercase.
    content = models.TextField(null = True)
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='authorID')  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='commentCount', blank=True, null=True)  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='publishDate')  # Field name made lowercase.
    visibility = models.TextField(null = True)
    linked_img_post = models.TextField("self", blank = True, null = True)

    class Meta:
        managed = True