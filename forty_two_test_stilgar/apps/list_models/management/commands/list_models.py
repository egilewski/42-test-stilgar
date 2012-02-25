from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in models.get_models():
            msg = '%s model with %d objects\n' % \
                              (model.__name__, model.objects.count())
            self.stdout.write(msg)
            self.stderr.write('error: ' + msg)
