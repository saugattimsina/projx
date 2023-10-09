from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from user.models import User
from .models import Subscription, UserSubcription
from binarytree.models import MLMMember,MLMBinary
# ,ForcedMatrix

from collections import deque



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



@receiver(pre_save, sender=User)
def generate_referal_code(sender, instance, **kwargs):
    if not instance.referal_code:
        referal_code = instance.username
        instance.referal_code = referal_code


'''
admin user is not being added to binary model that should 
be added tooo first need to finish the binary model


'''
@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            default_subscription = Subscription.objects.get(package_type='free')
            if default_subscription:
                UserSubcription.objects.create(user=instance, plan=default_subscription)

        if instance.is_superuser:
            MLMMember.add_root(user=instance, name=instance.username)
        else:
            parent = MLMMember.objects.get(user = instance.refered)
            parent.add_child(user=instance, name=instance.username,sponsor = parent)



        # forced_users = ForcedMatrix.objects.all()
        # if forced_users.count() == 0:
        #     ForcedMatrix.add_root(name=instance)
        # else:
        #     parent2 = ForcedMatrix.objects.get(name = instance.refered)
        #     number_childs = parent.get_children_count()
        #     if number_childs < 3:
        #         parent2.add_child(name=instance)
        #     else:
        #         total_refered = parent.get_children()
        #         if total_refered%2 == 1:
        #             """move to left"""

        #         else:
        #             """move to right"""
        
        if not instance.is_superuser:
            binary_members = MLMBinary.objects.all()
            if binary_members.count() == 0:
                print("yaha1")
                MLMBinary.add_root(name=instance)
            else:
                print('yaha2')
                parentbinary = MLMBinary.objects.get(name = instance.refered)
                print("parent_binary",parentbinary)
                # siblings = parent.get_siblings()
                decends = parentbinary.get_children_count()
                print("munber of decends ",decends)
                if not decends :
                    print('yah3')
                    x = parentbinary.add_child(name=instance,parent=parentbinary)
                    parentbinary.user_left = x
                    parentbinary.save()
                elif (decends == 1):
                    print('yah44')

                    x = parentbinary.add_child(name=instance,parent=parentbinary)
                    parentbinary.user_right = x
                    parentbinary.save()
                elif(decends == 2):
                    print('yah5')
                    get_all_childs = parent.get_children_count()
                    # print(get_all_childs)
                    if get_all_childs % 2 == 1:
                        print('yah6')
                        left_user = parentbinary.get_children().first()
                        node = get_all_nodes_bfs(left_user)
                        spilled_parent = node['node']
                        child_num = node['children']
                        if child_num == 0:
                            x =  spilled_parent.add_child(name=instance,parent=spilled_parent)
                            spilled_parent.user_left = x
                            spilled_parent.save()
                        elif child_num == 1:
                            x =  spilled_parent.add_child(name=instance,parent=spilled_parent)
                            spilled_parent.user_right = x
                            spilled_parent.save()
                        print("left user",left_user)
                        """ need to add user in the left wing """
                    else:
                        print('yah7')
                        right_user = parentbinary.get_children().last()
                        node = get_all_nodes_bfs(right_user)
                        spilled_parent = node['node']
                        child_num = node['children']
                        if child_num == 0:
                            x =  spilled_parent.add_child(name=instance,parent=spilled_parent)
                            spilled_parent.user_left = x
                            spilled_parent.save()
                        elif child_num == 1:
                            x =  spilled_parent.add_child(name=instance,parent=spilled_parent)
                            spilled_parent.user_right = x
                            spilled_parent.save()
                    
                        """ need to add user in the right wing """
                else:
                    print('oops something went wrong')

                
                
            
