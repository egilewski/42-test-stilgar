"""Model helpers for forty_two_test_stilgar."""
from django.db.models import Model


class ExtendedModel(Model):
    """Model with reusable custom methods."""
    def get_fields(self, exclude=('id',)):
        """Return dict of all fields except listed to be excluded and empty."""
        fields = {}
        for field in self._meta.fields:
            if not field.name in exclude and getattr(self, field.name):
                fields[field.name] = getattr(self, field.name)
        return fields

    fields = property(get_fields)
    """List of all fields except "id"."""

    # pylint: disable=W0232,R0903
    class Meta:
        """Extended model meta subclass for Django flags."""
        abstract = True
