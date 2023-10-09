from django.shortcuts import render
from .models import MLMMember,MLMBinary
import pprint
from collections import deque

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
    priority_node = {"node":None,"children":None}

    while queue:
        node = queue.popleft()  # Get the first node from the queue
        nodes.append(node)

        # Add all children of the current node to the queue
        children = node.get_children()

        if child is None and children.count() >0:
            child = children[0]
        if child and child == node:
            level += 1

            child = children[0] if children.count() >0 else None
            if priority_node['children'] is not None:
                # priority_node["children"] = 1
                print("triggered")
                break
        queue.extend(children)

        if children.count() == 0:
            priority_node["node"] = node
            priority_node["children"] = 0

            break
        elif(children.count() == 1):
            if priority_node['node']:
                continue
            else:
                priority_node["node"] = node
                priority_node["children"] = 1
                # priority_node["children"] = 1

    print("priority",priority_node)

    return priority_node


# def remove_node_and_transfer_children(root, target_id):
#     if root is None:
#         return None
    
#     if root.id == target_id:
#         # Found the target node, perform the removal and replacement
#         left_child = root.user_left
#         if left_child:
#             # Transfer left child's children to the root
#             root.user_left = left_child.user_left
#             root.user_right = left_child.user_right
#             root.save()
#             # Recursively delete the left child
#             remove_node_and_transfer_children(left_child, left_child.id)
#         else:
#             # If there is no left child, simply remove the node
#             root.delete()
#         return root

#     # Recursively search for the target node in the left and right subtrees
#     root.user_left = remove_node_and_transfer_children(root.user_left, target_id)
#     root.user_right = remove_node_and_transfer_children(root.user_right, target_id)
    
#     return root

# Usage:
# Replace 'root_node' with the root of your binary tree
# # Replace 'target_id' with the ID of the node you want to remove
# root_node = MLMBinary.objects.get(id=1)
# target_id = 3
# remove_node_and_transfer_children(root_node, target_id)




def treeview(request):
    binary_members = MLMBinary.get_descendants_group_count(parent=None)
    # pprint.pprint(binary_members)
    if binary_members:
        node = binary_members[0]
        priority = get_all_nodes_bfs(node)
        
    
    # Create a list to store the hierarchical data with referenced items resolved
    # car = {}
    # for users in binary_members:
    #     print(users['level'])
        
    return render(request, 'treeview.html')


