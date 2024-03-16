from django.db import models
from authentication.models import Author

# Create your models here.
class Notification(models.Model):
    type = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author')
    created_at = models.DateTimeField(auto_now_add=True)

