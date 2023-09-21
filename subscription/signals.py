from django.dispatch import receiver
from django.db.models.signals import post_save

from user.models import User
from .models import Subscription, UserSubcription


@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        default_subscription = Subscription.objects.get(package_type='free')
        if default_subscription:
            UserSubcription.objects.create(user=instance, plan=default_subscription)
