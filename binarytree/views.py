from django.shortcuts import render
from .models import MLMMember,MLMBinary
import pprint
from collections import deque
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

def treeview(request):
    binary_members = MLMBinary.get_descendants_group_count(parent=None)
    # pprint.pprint(binary_members)
    node = binary_members[0]
    priority = get_all_nodes_bfs(node)
    
    
    # Create a list to store the hierarchical data with referenced items resolved
    # car = {}
    # for users in binary_members:
    #     print(users['level'])
        
    return render(request, 'treeview.html')
