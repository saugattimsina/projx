from django.db.models.signals import post_save
from user.models import User
from django.dispatch import receiver
from binarytree.models import MLMRank, UserRank
from binarytree.determine_rank import find_all_parent_node


@receiver(post_save, sender=User)
def create_default_rank(sender, instance, created, **kwargs):
    if created:
        try:

            default_rank = MLMRank.objects.get(equivalent_name="Unranked")
            
        except MLMRank.DoesNotExist:
            default_rank = MLMRank.objects.create(
                equivalent_name="Unranked",
                min_referrals=0,
                max_referrals=2,
                min_team_size=0,
                max_team_size=2,
            )
        if default_rank:
            x = UserRank.objects.create(user=instance, rank=default_rank)
            user = User.objects.get(id=x.user.id)
            find_all_parent_node(user=user)
