from django.db.models.signals import pre_save
from django.dispatch import receiver
from lms.utilities import unique_slug_generator
from . import models


@receiver(pre_save, sender=models.Document)
def document_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.call_no:
        # todo generate call_no here
        ...


