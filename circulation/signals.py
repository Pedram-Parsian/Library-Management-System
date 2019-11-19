from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_save, sender=models.Issue)
def issue_pre_save_receiver(sender, instance: models.Issue, **kwargs):
    # if not instance.pk:
    #     instance.status = models.Issue.PENDING
    # else:
    #     # the max_due_date will have either the *most far* due date or the instance due_date itself,
    #     # if there is not any renews for the issue:
    #     max_due_date = instance.renew_set.order_by(
    #         '-due_date').first().due_date if instance.renew_set.exists() else instance.due_date
    #     if instance.returned_date:
    #         # user has returned the document
    #         if instance.returned_date > max_due_date:
    #             instance.status = models.Issue.DONE_OVERDUE
    #         else:
    #             instance.status = models.Issue.DONE
    #     else:
    #         # user has not returned document
    #         if timezone.now() >= max_due_date:
    #             instance.status = models.Issue.PENDING_OVERDUE
    #         else:
    #             instance.status = models.Issue.PENDING
    instance.set_status()


@receiver(post_save, sender=models.Issue)
def issue_post_save_receiver(sender, instance: models.Issue, **kwargs):
    instance.document.set_status()


@receiver(pre_save, sender=models.Reserve)
def reserve_pre_save_receiver(sender, instance: models.Reserve, **kwargs):
    instance.set_status()


@receiver(post_save, sender=models.Reserve)
def reserve_post_save_receiver(sender, instance: models.Reserve, **kwargs):
    instance.document.set_status()


@receiver(post_save, sender=models.Renew)
def reserve_post_save_receiver(sender, instance: models.Renew, **kwargs):
    instance.issue.set_status()

# todo search: single post_save signal that has multiple senders
