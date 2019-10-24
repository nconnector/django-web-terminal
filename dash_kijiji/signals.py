from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def announce_new_user(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       "event": "New User",
                       "username": instance.username,
                       })






class StdoutManager:
    output = Signal(providing_args=["toppings", "size"])

    def new_stdout(self, group, data):
        self.output.send(sender=self.__class__, group=group, data=data)
