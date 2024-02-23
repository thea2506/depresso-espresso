from django.db import models
from authentication.models import Author

# Create your models here.
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