"""Models for user profile app."""
from django.db import models
from forty_two_test_stilgar.helpers.model_helpers import ExtendedModel

class Profile(ExtendedModel):
    """User profile model."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=50)
    contacts = models.TextField()
