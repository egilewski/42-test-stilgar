"""Test for model object actions logging. Tests logging with all project
models, creating, updating and deleting records. Skips models with
foregign and one-to-one fields for simplicity."""
import datetime
from tddspry.django import DatabaseTestCase
from django.db import models
from forty_two_test_stilgar.apps.model_log.models import ModelLog


# pylint: disable=R0904
class TestModelLogger(DatabaseTestCase):
    def test_model_logger_on_all_models(self):
        for model in models.get_models():
            if model == ModelLog:
                continue
            # Populate instance with some values to not get notnull error.
            fields = generate_default_values_for_fields(model)
            if not fields:
                continue
            test_obj = model(**fields)
            # Test create.
            test_obj.save()
            log_fields = {
                'model': model.__name__,
                'object_pk': test_obj.pk,
            }
            if isinstance(test_obj.pk, int):
                log_fields['object_id'] = int(test_obj.pk)
            log_fields['action'] = 'create'
            self.assert_read(ModelLog, **log_fields)
            # Test update.
            test_obj.save()
            log_fields['action'] = 'edit'
            self.assert_read(ModelLog, **log_fields)
            # Test delete.
            test_obj.delete()
            log_fields['action'] = 'delete'
            self.assert_read(ModelLog, **log_fields)

def generate_default_values_for_fields(model):
    fields = {}
    for field in model._meta.fields:
        if not field.blank:
            if isinstance(field, models.DateField):
                fields[field.name] = datetime.datetime.now()
            elif isinstance(field, models.CharField) \
                    or isinstance(field, models.TextField):
                fields[field.name] = 'test'
            elif isinstance(field, models.IntegerField):
                fields[field.name] = 1
            else:
                # Skip test for this model.
                return None
    return fields
