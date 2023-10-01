from django.shortcuts import render
from django.http import HttpResponse
from .models import MLMMember, MLMBinary, MLMRank, UserRank

from user.models import User  # Import the User model


# Create your views here.
def determinerank(user):
    x = MLMMember.objects.get(user=user)
    referred = x.get_children_count()
    print(referred)
    team_size = x.get_descendant_count()
    print(team_size)
    ranks = MLMRank.objects.filter(
        min_referrals__lte=5,
        max_referrals__gte=5,
        min_team_size__lte=100,
        max_team_size__gte=100,
    ).first()
    if ranks:
        try:
            print("hi")
            user_rank = UserRank.objects.get(user=user).rank.name
            print(ranks, user_rank)
            if ranks.name != user_rank:
                pass
        except:
            print("not found")
        return ranks.name
    else:
        ranks = MLMRank.objects.filter(
            min_referrals=0,
        ).first()
        return ranks.name


def determine_rank_in_tree(request):
    x = MLMMember.objects.get(name="symbol")
    ancestors = x.get_ancestors()

    for ancestor in ancestors:
        print(ancestor.user)
        print(determinerank(ancestor.user))
    return HttpResponse("ok")
