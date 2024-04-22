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

    def __str__(self):
        return self.name.username if self.name else "Empty"


class MLMRank(models.Model):
    rank_image = models.ImageField(
        upload_to="uploads/ranks/%Y/%m/%d/", null=True, blank=True
    )
    rank_choice = (
        ("Pawn", "Pawn"),
        ("Knight", "Knight"),
        ("Bishop", "Bishop"),
        ("Rook", "Rook"),
        ("Queen", "Queen"),
        ("King", "King"),
    )
    equivalent_name = models.CharField(
        max_length=25, choices=rank_choice, default="Pawn"
    )
    rank_name = models.CharField(max_length=25, null=True, blank=True)
    direct_referrals = models.IntegerField(default=0)
    active_members = models.IntegerField(default=0)
    separate_enroller_tree_conditions = models.JSONField(default=dict)

    # def __str__(self):
    #     return self.rank_name


class UserRank(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey(MLMRank, on_delete=models.SET_NULL, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.user} {self.rank.equivalent_name}"


class BinaryParents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parents = models.ManyToManyField(MLMBinary, null=True, blank=True)
