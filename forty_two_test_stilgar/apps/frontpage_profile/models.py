from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()
