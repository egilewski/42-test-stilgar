"""Models for user profile app."""
from django.db import models
from forty_two_test_stilgar.helpers.model_helpers import ExtendedModel

class Profile(ExtendedModel):
    """User profile model."""
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=64)
    contacts = models.TextField()
    image = models.ImageField(upload_to='profile', max_length=512, blank=True)
