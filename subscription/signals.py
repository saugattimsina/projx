from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from user.models import User
from .models import Subscription, UserSubcription, UserSubPaymentHistory
from binarytree.models import MLMMember, MLMBinary, BinaryParents
from subscription.enroller_commision import calculate_commission
from subscription.matrix_commision import calculate_matrix_commission
from binarytree.determine_rank import find_all_parent_node

# ,ForcedMatrix

from collections import deque


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


@receiver(pre_save, sender=User)
def generate_referal_code(sender, instance, **kwargs):
    if not instance.referal_code:
        referal_code = instance.username
        instance.referal_code = referal_code


"""
admin user is not being added to binary model that should 
be added tooo first need to finish the binary model


"""


@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        # if not instance.is_superuser:

        # try:
        #     default_subscription = Subscription.objects.get(package_type="free")
        # except Subscription.DoesNotExist:
        #     default_subscription = Subscription.objects.create(
        #         package_type="free",
        #         price=0,
        #         time_in_days=365,
        #         time_in_months=12,
        #         package_name="Free",
        #     )
        # if default_subscription:
        #     UserSubcription.objects.create(user=instance, plan=default_subscription)
        if instance.is_superuser:
            MLMMember.add_root(user=instance, name=instance.username)
            MLMBinary.add_root(name=instance)


@receiver(post_save, sender=UserSubcription)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        pakage_type = instance.plan.package_type
        if pakage_type != "free":
            print("user subscribed")
            user.is_suscribed = True
            user.save()

        if user.is_superuser:
            MLMMember.add_root(user=user, name=user.username)
        else:
            if user.is_suscribed:
                if not MLMMember.objects.filter(user=user).exists():
                    print("yaha puge ko xa")
                    parent = MLMMember.objects.get(user=user.refered)
                    parent.add_child(user=user, name=user.username, sponsor=parent)

        if not user.is_superuser:
            if user.is_suscribed:
                if not MLMBinary.objects.filter(name=user).exists():
                    binary_members = MLMBinary.objects.all()
                    if binary_members.count() == 0:
                        print("yaha1")

                        MLMBinary.add_root(name=user)
                    else:
                        print("yaha2")
                        parentbinary = MLMBinary.objects.get(name=user.refered)
                        print("parent_binary", parentbinary)
                        # siblings = parent.get_siblings()
                        decends = parentbinary.get_children_count()
                        print("munber of decends ", decends)
                        if not decends:
                            print("yah3")
                            x = parentbinary.add_child(name=user, parent=parentbinary)
                            parentbinary.user_left = x
                            parentbinary.save()
                        elif decends == 1:
                            print("yah44")

                            x = parentbinary.add_child(name=user, parent=parentbinary)
                            parentbinary.user_right = x
                            parentbinary.save()
                        elif decends == 2:
                            print("yah5")
                            get_all_childs = parent.get_children_count()
                            # print(get_all_childs)
                            if get_all_childs % 2 == 1:
                                print("yah6")
                                left_user = parentbinary.get_children().first()
                                node = get_all_nodes_bfs(left_user)
                                spilled_parent = node["node"]
                                child_num = node["children"]
                                if child_num == 0:
                                    x = spilled_parent.add_child(
                                        name=user, parent=spilled_parent
                                    )
                                    spilled_parent.user_left = x
                                    spilled_parent.save()
                                elif child_num == 1:
                                    x = spilled_parent.add_child(
                                        name=user, parent=spilled_parent
                                    )
                                    spilled_parent.user_right = x
                                    spilled_parent.save()
                                print("left user", left_user)
                                """ need to add user in the left wing """
                            else:
                                print("yah7")
                                right_user = parentbinary.get_children().last()
                                node = get_all_nodes_bfs(right_user)
                                spilled_parent = node["node"]
                                child_num = node["children"]
                                if child_num == 0:
                                    x = spilled_parent.add_child(
                                        name=user, parent=spilled_parent
                                    )
                                    spilled_parent.user_left = x
                                    spilled_parent.save()
                                elif child_num == 1:
                                    x = spilled_parent.add_child(
                                        name=user, parent=spilled_parent
                                    )
                                    spilled_parent.user_right = x
                                    spilled_parent.save()

                                """ need to add user in the right wing """
                        else:
                            print("oops something went wrong")
                user = User.objects.get(id=user.id)
                find_all_parent_node(user=user)


@receiver(post_save, sender=UserSubcription)
def enrollment_commision(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user.is_suscribed:
            no_sub_payment = UserSubPaymentHistory.objects.filter(user=user).count()
            if no_sub_payment == 1:
                amount = instance.plan.price
                x = MLMMember.objects.get(user=user)
                reffered_by = user.refered
                refered_user = user
                ancestors = x.get_ancestors()
                calculate_commission(
                    ancestors=ancestors,
                    amount=amount,
                    reffered_by=reffered_by,
                    refered_user=refered_user,
                )
                x = MLMBinary.objects.get(name=user)
                ancestors = x.get_ancestors()
                for ancestor in ancestors:
                    try:
                        binary_parent = BinaryParents.objects.get(user=user)
                    except:
                        binary_parent = BinaryParents.objects.create(user=user)
                    binary_parent.parents.add(ancestor)
                    binary_parent.save()
            elif no_sub_payment > 1:
                print(4)
                amount = instance.plan.price
                calculate_matrix_commission(user=user, amount=amount)
