from django.db import models

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