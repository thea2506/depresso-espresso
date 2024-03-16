from django.db import models
from authentication.models import Author

# Create your models here.
class Notification(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

