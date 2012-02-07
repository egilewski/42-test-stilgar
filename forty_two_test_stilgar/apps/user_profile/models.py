"""Models for user profile app."""
from django.db import models


class Profile(models.Model):
    """User profile model."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=50)
    contacts = models.TextField()

    def fields(self):
        """Returns list of all fields except "id"."""
        return [getattr(self, field.name) \
                for field in self._meta.fields if field.name != 'id']
