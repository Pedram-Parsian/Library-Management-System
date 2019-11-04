from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from documents.models import Document
from lms.utilities import unique_slug_generator
from . import models


@receiver(pre_save, sender=models.Document)
def document_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.call_no:
        # todo generate call_no here
        ...


@receiver(post_save, sender=models.Review)
def review_post_save_receiver(sender, instance, **kwargs):
    Document.recalculate_rating(instance.document_id)
