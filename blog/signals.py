from django.db.models.signals import pre_save
from django.dispatch import receiver
from pedramparsian.utilities import unique_slug_generator
from . import models

@receiver(pre_save, sender=models.Post)
def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=models.PostTag)
def post_tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=models.PostCategory)
def post_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
