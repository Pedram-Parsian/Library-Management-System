from django.db.models.signals import pre_save
from django.dispatch import receiver

from lms.utilities import unique_number_generator
from . import models


@receiver(pre_save, sender=models.Payment)
def payment_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.successful and not instance.reference_num:
        instance.reference_num = unique_number_generator(instance)
