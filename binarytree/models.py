from user.models import User  # Import the User model
from django.db import models
from treebeard.mp_tree import MP_Node
from treebeard.ns_tree import NS_Node


class MLMMember(MP_Node):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sponsor = models.ForeignKey(
        "MLMMember", on_delete=models.SET_NULL, null=True, blank=True
    )
    # Other fields to represent relevant information about the MLM member

    def __str__(self):
        return self.name

    # def get_parents_up_to_level(self, level):
    #     parents = []
    #     current_node = self.parent

    #     while current_node and level > 0:
    #         parents.append(current_node)
    #         current_node = current_node.parent
    #         level -= 1

    #     return parents


class MLMBinary(MP_Node):
    # node_order_by = ['']
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Parent binary node
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parent_user",
    )

    # Left child binary node
    user_left = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="left"
    )

    # Right child binary node
    user_right = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="right"
    )

    # Other fields to represent relevant information about the MLM member

    # def __str__(self):
    #     return self.name.username


class MLMRank(models.Model):
    name = models.CharField(max_length=150)
    min_referrals = models.IntegerField(null=True, blank=True)
    max_referrals = models.IntegerField(null=True, blank=True)
    min_team_size = models.IntegerField(null=True, blank=True)
    max_team_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserRank(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey(MLMRank, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.rank.name}"


class BinaryParents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parents = models.ManyToManyField(MLMBinary)
