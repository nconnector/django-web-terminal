from django.dispatch import receiver
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save
from asgiref.sync import async_to_sync

from .models import Case


@receiver(pre_save, sender=Case)
def case_edited(sender, instance, **kwargs):
    """case set up or log has been appended"""
    # if update_fields:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "logging", {"type": "case.logging",  # logginig - group name; type - case_logging in consumers.py
                    "event": "log edited",
                    "last_log": instance.log_last(),
                    })
