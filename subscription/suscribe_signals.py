from django.dispatch import receiver
from django.db.models.signals import pre_save

from user.models import User
from .models import Subscription, UserSubcription

from datetime import datetime,timedelta

'''
testing remaining
'''
@receiver(pre_save, sender=UserSubcription)
def add_user_subscription(sender, instance, **kwargs):
    '''
    whwn user suscribe to a plan here we will
    add days and calculate the days and add to the end date
    '''
    if not instance.is_superuser:
        user_current_subscription = UserSubcription.objects.filter(user=instance.user, plan__package_type = 'paid').order_by('-id')
        if user_current_subscription:
            user_package = user_current_subscription.first()
            time_to_expire = user_package.end_date - datetime.now()
            # if time_to_expire.days > 0:
            instance.end_date = datetime.now() + timedelta(int(time_to_expire)) + timedelta(days=int(instance.plan.time_in_days))
            # user_package.end_date = user_package.end_date + timedelta(days=int(instance.plan.time_in_days))
            # user_package.save()
            # instance.save()

        else:
            days_to_add = int(instance.plan.time_in_days)
            end_date = (datetime.now()+timedelta(days=days_to_add))
            instance.end_date = end_date 
            # instance.save()

        # if not instance.referal_code:
        #     referal_code = instance.username
        #     instance.referal_code = referal_code

