# from django.db.models.signals import post_save
# from user.models import User
# from django.dispatch import receiver


# @receiver(post_save, sender=User)
# def create_default_subscription(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_superuser:
#             print('supwruser created')