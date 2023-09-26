from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from user.models import User
from .models import Subscription, UserSubcription
from binarytree.models import MLMMember




@receiver(pre_save, sender=User)
def generate_referal_code(sender, instance, **kwargs):
    if not instance.referal_code:
        referal_code = instance.username
        instance.referal_code = referal_code



@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        default_subscription = Subscription.objects.get(package_type='free')
        if default_subscription:
            UserSubcription.objects.create(user=instance, plan=default_subscription)

        if instance.is_superuser:
            MLMMember.add_root(user=instance, name=instance.username)
        else:
            parent = MLMMember.objects.get(user = instance.refered)
            parent.add_child(user=instance, name=instance.username,sponsor = parent)