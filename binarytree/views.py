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
#     print("childrens ",childrens)
#     if len(childrens) == 0:
#         """
#         delete the node continue
#         """
#         return
#     elif(len(childrens) == 1):

#         for child in childrens:

#             print("child",child)
#             nodes.extend(get_all_nodes_recursive(child))
#         return nodes

# binary_members = MLMBinary.objects.all()
# get_all_nodes_recursive(binary_members[0])


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

    # return render(request, "treeview.html")


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


def weekly_fast_start_commissions(ancestors):
    membership_amount = 40
    level = len(ancestors)
    for ancestor in ancestors:
        user = ancestor.user
        rank = UserRank.objects.get(user=user).rank.name
        print("user :", user)
        print("rank :", rank)
        print("level :", level)
        if level == 1:
            print(f"commision 50%")
        elif level == 2 and (
            rank == "Bronze"
            or rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision 10%")
        elif (level == 3 or level == 4) and (
            rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision 5%")
        elif level == 5 and (rank == "Platinum" or rank == "Diamond" or rank == "Gold"):
            print(f"commision {membership_amount*0.03}")
        elif level == 6 and (rank == "Platinum" or rank == "Diamond" or rank == "Gold"):
            print(f"commision {membership_amount*0.02}")
        elif level == 7 and (rank == "Platinum" or rank == "Diamond"):
            print(f"commision {membership_amount*0.02}")
        elif level == 8 and (rank == "Platinum" or rank == "Diamond"):
            print(f"commision {membership_amount*0.01}")
        elif (level == 9 or level == 10) and rank == "Diamond":
            print(f"commision {membership_amount*0.01}")
        else:
            print("no commisions")
        level = level - 1


def determine_rank_in_tree(request):
    user = User.objects.get(id=31)
    print(user)
    x = MLMMember.objects.get(user=user)
    ancestors = x.get_ancestors()
    print(ancestors)
    weekly_fast_start_commissions(ancestors)
    # for ancestor in ancestors:
    #     print(ancestor.user)
    #     print(determinerank(ancestor.user))
    return HttpResponse("ok")
