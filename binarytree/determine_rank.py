from binarytree.models import MLMMember, MLMRank, MLMBinary, UserRank
from django.db.models import Q


# def determinerank(ancestors):
#     if len(ancestors) != 0:
#         for ancestor in ancestors:
#             user = ancestor.user
#             user_rank = UserRank.objects.get(user=user)
#             print(user)
#             print(user_rank.rank)
#             x = MLMMember.objects.get(user=user)
#             referrals = x.get_children_count()
#             team_size = x.get_descendant_count()
#             # Find the MLMRank object that matches the user's referrals.
#             rank_by_referrals = MLMRank.objects.filter(
#                 min_referrals__lte=referrals,
#                 max_referrals__gte=referrals,
#             ).first()

#             # Find the MLMRank object that matches the user's team size.
#             rank_by_team_size = MLMRank.objects.filter(
#                 min_team_size__lte=team_size,
#                 max_team_size__gte=team_size,
#             ).first()
#             # Check if rank_by_referrals is None, and if so, handle this case.
#             if rank_by_referrals is None:
#                 print("Rank by referrals is None. Handle this case.")
#                 continue  # Skip this user

#             if rank_by_team_size is None:
#                 print("Rank by team size is None. Handle this case.")
#                 continue

#             # If the user's referrals and team size match the same rank, return that rank.
#             if rank_by_referrals == rank_by_team_size:
#                 print(rank_by_referrals)
#                 user_rank.rank = rank_by_referrals
#                 user_rank.save()

#             # If the user's referrals and team size do not match the same rank, return the rank with the higher minimum value.
#             elif rank_by_referrals.min_referrals < rank_by_team_size.min_referrals:
#                 print(rank_by_referrals)
#                 user_rank.rank = rank_by_referrals
#                 user_rank.save()

#             else:
#                 print(rank_by_team_size)
#                 user_rank.rank = rank_by_team_size
#                 user_rank.save()
#             print(user_rank.rank)
#     else:
#         print("empty")


def find_children_rank(descendants):
    if len(descendants) != 0:
        Knight = 0
        Bishop = 0
        Rook = 0
        Queen = 0
        for descendant in descendants:
            user = descendant.name
            user_rank = UserRank.objects.get(user=user)
            if user_rank.rank.equivalent_name == "Knight":
                Knight += 1
            elif user_rank.rank.equivalent_name == "Bishop":
                Bishop += 1
            elif user_rank.rank.equivalent_name == "Rook":
                Rook += 1
            elif user_rank.rank.equivalent_name == "Queen":
                Queen += 1
        return Knight, Bishop, Rook, Queen


def find_active_member(mlmmembers):
    children_count = mlmmembers.get_children_count()
    children = mlmmembers.get_children()
    descendant_child_count = 0
    if children_count != 0:
        for child in children:
            child_descendant_count = child.get_descendant_count()
            if child_descendant_count > 30:
                descendant_child_count += 30
            else:
                descendant_child_count += child_descendant_count
    active_member = int(children_count) + descendant_child_count
    return active_member


def determine_rank(ancestors):
    if len(ancestors) != 0:
        for ancestor in ancestors:
            user = ancestor.name
            print(user)
            user_rank = UserRank.objects.get(user=user)
            print("old rank", user_rank.rank.equivalent_name)
            mlmmembers = MLMMember.objects.get(user=user)
            mlmbinary = MLMBinary.objects.get(name=user)
            direct_referrals = mlmmembers.get_children_count()
            active_members = mlmbinary.get_descendant_count()
            descendants = mlmbinary.get_descendants()

            Knight, Bishop, Rook, Queen = find_children_rank(descendants)

            active_member = find_active_member(mlmmembers)

            if Queen >= 3 or active_member >= 33000:
                rank = MLMRank.objects.get(equivalent_name="King")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()
            elif Rook >= 3 or (active_member >= 1500 and active_member < 33000):
                rank = MLMRank.objects.get(equivalent_name="Queen")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()
            elif (
                (
                    direct_referrals >= 30
                    and (active_members <= 300 and active_members > 100)
                )
                or Bishop >= 3
                or active_member >= 300
            ):
                rank = MLMRank.objects.get(equivalent_name="Rook")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()
            elif (
                (
                    direct_referrals >= 10
                    and (active_members <= 100 and active_members > 20)
                )
                or Knight >= 3
                or active_member >= 100
            ):
                rank = MLMRank.objects.get(equivalent_name="Bishop")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()
            elif direct_referrals >= 5 and active_members <= 20:
                rank = MLMRank.objects.get(equivalent_name="Knight")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()
            else:
                rank = MLMRank.objects.get(equivalent_name="Pawn")
                print("new rank: ", rank.equivalent_name)
                user_rank.rank = rank
                user_rank.save()

    else:
        print("No parents found")


def find_all_parent_node(user):
    x = MLMBinary.objects.get(name=user)
    ancestors = x.get_ancestors()
    determine_rank(ancestors)


def create_parents_binary(user):
    binary_pos = MLMBinary.objects.filter(name=user)
    if binary_pos.exists():
        ancestors = binary_pos[0].get_ancestors()
        print(ancestors)

    else:
        return None
