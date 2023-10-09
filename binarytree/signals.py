from django.db.models.signals import post_save
from user.models import User
from django.dispatch import receiver
from binarytree.models import MLMRank, UserRank


# @receiver(post_save, sender=User)
# def create_default_rank(sender, instance, created, **kwargs):
#     if created:
#         default_rank = MLMRank.objects.get(team_size=0)
#         if default_rank:
#             UserRank.objects.create(user=instance, rank=default_rank)
