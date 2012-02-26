from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class ModelLog(models.Model):
    model = models.TextField(max_length=128)
    action = models.TextField(max_length=6)
    # Not ForeignKey because it's can be deleted already.
    object_id = models.IntegerField()
    object_pk = models.CharField(max_length=255)


@receiver(post_save)
def model_log_save_listener(sender, instance, created, **kwargs):
    if sender == ModelLog:
        return
    if created:
        action = 'create'
    else:
        action = 'edit'
    object_pk = instance.pk
    object_id = 0
    if isinstance(object_pk, int):
        object_id = int(object_pk)
    log = ModelLog(model=sender.__name__, action=action,
                   object_id=object_id, object_pk=object_pk)
    log.save()

@receiver(post_delete)
def model_log_delete_listener(sender, instance, **kwargs):
    if sender == ModelLog:
        return
    object_pk = instance.pk
    object_id = 0
    if isinstance(object_pk, int):
        object_id = int(object_pk)
    log = ModelLog(model=sender.__name__, action='delete',
                   object_id=object_id, object_pk=object_pk)
    log.save()
