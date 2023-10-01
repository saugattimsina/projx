from binarytree.models import MLMMember, MLMRank, UserRank
from django.db.models import Q


def determinerank(ancestors):
    if len(ancestors) != 0:
        for ancestor in ancestors:
            user = ancestor.user
            user_rank = UserRank.objects.get(user=user)
            print(user)
            print(user_rank.rank)
            x = MLMMember.objects.get(user=user)
            referrals = x.get_children_count()
            team_size = x.get_descendant_count()
            # Find the MLMRank object that matches the user's referrals.
            rank_by_referrals = MLMRank.objects.filter(
                min_referrals__lte=referrals,
                max_referrals__gte=referrals,
            ).first()

            # Find the MLMRank object that matches the user's team size.
            rank_by_team_size = MLMRank.objects.filter(
                min_team_size__lte=team_size,
                max_team_size__gte=team_size,
            ).first()
            # If the user's referrals and team size match the same rank, return that rank.
            if rank_by_referrals == rank_by_team_size:
                print(rank_by_referrals)
                user_rank.rank = rank_by_referrals
                user_rank.save()

            # If the user's referrals and team size do not match the same rank, return the rank with the higher minimum value.
            elif rank_by_referrals.min_referrals < rank_by_team_size.min_referrals:
                print(rank_by_referrals)
                user_rank.rank = rank_by_referrals
                user_rank.save()

            else:
                print(rank_by_team_size)
                user_rank.rank = rank_by_team_size
                user_rank.save()
            print(user_rank.rank)
    else:
        print("empty")


def find_all_parent_node(user):
    x = MLMMember.objects.get(user=user)
    ancestors = x.get_ancestors()
    determinerank(ancestors)
