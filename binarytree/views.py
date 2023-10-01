from django.shortcuts import render
from .models import MLMMember, MLMBinary
import pprint
from collections import deque
from django.http import HttpResponse
from .models import MLMMember, MLMBinary, MLMRank, UserRank

from user.models import User  # Import the User model

# Create your views here.
# def get_all_nodes_recursive(node):
#     nodes = [node]
#     childrens = node.get_children()
#     # this code goes to the leftmost side first dfs but we need to go bfs
#     for child in childrens:
#         # if :
#         print("child",child)
#         # if :
#         nodes.extend(get_all_nodes_recursive(child))
#     return nodes


def get_all_nodes_bfs(root_node):
    nodes = []
    queue = deque([root_node])
    level = 1
    child = None
    priority_node = {"node": None, "children": None}

    while queue:
        node = queue.popleft()  # Get the first node from the queue
        nodes.append(node)

        # Add all children of the current node to the queue
        children = node.get_children()

        if child is None and children.count() > 0:
            child = children[0]
        if child and child == node:
            level += 1

            child = children[0] if children.count() > 0 else None
            if priority_node["children"] is not None:
                # priority_node["children"] = 1
                print("triggered")
                break
        queue.extend(children)

        if children.count() == 0:
            priority_node["node"] = node
            priority_node["children"] = 0

            break
        elif children.count() == 1:
            if priority_node["node"]:
                continue
            else:
                priority_node["node"] = node
                priority_node["children"] = 1
                # priority_node["children"] = 1

    print("priority", priority_node)

    return priority_node


def treeview(request):
    binary_members = MLMBinary.get_descendants_group_count(parent=None)
    # pprint.pprint(binary_members)
    node = binary_members[0]
    priority = get_all_nodes_bfs(node)

    # Create a list to store the hierarchical data with referenced items resolved
    # car = {}
    # for users in binary_members:
    #     print(users['level'])

    return render(request, "treeview.html")


# Create your views here.
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


def determine_rank_in_tree(request):
    user = User.objects.get(id=31)
    x = MLMMember.objects.get(user=user)
    ancestors = x.get_ancestors()
    determinerank(ancestors)
    return HttpResponse("ok")
