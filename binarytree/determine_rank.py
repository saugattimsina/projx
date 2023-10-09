from binarytree.models import MLMMember, MLMRank
from django.db.models import Q


def determinerank(user):
    x = MLMMember.objects.get(user=user)
    reffered = x.get_children_count()
    team_size = x.get_descendant_count()
    rank = MLMRank.objects.filter(
        min_referrals__lte=reffered,
        max_referrals__gte=reffered,
        min_team_size__lte=team_size,
        max_team_size__gte=team_size,
    )
    return rank


def find_all_parent_node(user):
    x = MLMMember.objects.get(user=user)
    ancestors = x.get_ancestors()
    for ancestor in ancestors:
        print(ancestor.user)
        determinerank(ancestor.user)
