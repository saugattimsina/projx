from .models import Order, UserActivePositions
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction


@receiver(post_save, sender=Order)
def send_trade_update(sender, instance, created, **kwargs):

    def send_update():
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.username}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_closed_trades",
            },
        )
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "closed_trades",
            },
        )

    transaction.on_commit(send_update)


@receiver(post_save, sender=UserActivePositions)
def send_active_trade_update(sender, instance, created, **kwargs):
    print("here")

    def send_update():
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.username}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_active_trades",
            },
        )

    transaction.on_commit(send_update)
