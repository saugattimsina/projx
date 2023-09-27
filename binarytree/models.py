from user.models import User  # Import the User model
from django.db import models
from treebeard.mp_tree import MP_Node

class MLMMember(MP_Node):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sponsor = models.ForeignKey('MLMMember', on_delete=models.SET_NULL, null=True, blank=True)
    # Other fields to represent relevant information about the MLM member
    
    def __str__(self):
        return self.name

    def get_parents_up_to_level(self, level):
        parents = []
        current_node = self.parent

        while current_node and level > 0:
            parents.append(current_node)
            current_node = current_node.parent
            level -= 1

        return parents