"""Model helpers for forty_two_test_stilgar."""
from django.db.models import Model


class ExtendedModel(Model):
    """Model with reusable custom methods."""
    def get_fields(self, exclude=('id',)):
        """Returns list of all fields except "id"."""
        # pylint: disable=E1101
        return [getattr(self, field.name) \
                for field in self._meta.fields if not field.name in exclude]

    fields = property(get_fields)
    """List of all fields except "id"."""

    # pylint: disable=W0232,R0903
    class Meta:
        """Extended model meta subclass for Django flags."""
        abstract = True
