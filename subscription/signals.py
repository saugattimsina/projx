from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from user.models import User
from .models import Subscription, UserSubcription
from binarytree.models import MLMMember,MLMBinary




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
        default_subscription = Subscription.objects.get(package_type='free')
        if default_subscription:
            UserSubcription.objects.create(user=instance, plan=default_subscription)

        if instance.is_superuser:
            MLMMember.add_root(user=instance, name=instance.username)
        else:
            parent = MLMMember.objects.get(user = instance.refered)
            parent.add_child(user=instance, name=instance.username,sponsor = parent)

        binary_members = MLMBinary.objects.all()
        if binary_members.count() == 0:
            print("yaha1")
            MLMBinary.add_root(name=instance)
        else:
            print('yaha2')
            parent = MLMBinary.objects.get(name = instance.refered)
            # siblings = parent.get_siblings()
            decends = parent.get_children_count()
            print("munber of decends ",decends)
            if not decends :
                print('yah3')
                x = parent.add_child(name=instance,parent=parent)
                parent.user_left = x
                parent.save()
            elif (decends == 1):
                print('yah44')

                x = parent.add_child(name=instance,parent=parent)
                parent.user_right = x
                parent.save()
            elif(decends == 2):
                print('yah5')

                left_user = parent.get_children().first()
                right_user = parent.get_children().last()
                users_left_side = left_user.get_descendant_count()
                users_right_side = right_user.get_descendant_count()

                print("users count left and right",users_left_side,users_right_side)
                print("user_to_my left and right",left_user,right_user)
               
            
        
