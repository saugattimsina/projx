from django.dispatch import receiver
from django.db.models.signals import pre_save

from user.models import User
from .models import Subscription, UserSubcription

from datetime import datetime, timedelta
from django.utils import timezone

"""
testing remaining
"""


@receiver(pre_save, sender=UserSubcription)
def add_user_subscription(sender, instance, **kwargs):
    """
    whwn user suscribe to a plan here we will
    add days and calculate the days and add to the end date
    """
    start_date = timezone.now()
    if instance.plan.time_in_days:
        end_date = start_date + timedelta(days=int(instance.plan.time_in_days))
    elif instance.plan.time_in_months:
        end_date = start_date + timedelta(
            days=30 * int(instance.plan.time_in_months)
        )  # Assuming 30 days per month
    else:
        # Handle the case where both time_in_days and time_in_months are empty
        end_date = start_date
    instance.end_date = end_date
