from django.shortcuts import render
from binarytree.models import MLMBinary, MLMMember
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def get_descendants_up_to_2_levels(node, root):
    descendants = []
    for child in node.get_children():
        binarytree = {}  # Create a new dictionary for each child
        binarytree["level"] = 1
        binarytree["user"] = child.name.username
        children = []
        for sub_child in child.get_children():
            child_data = {
                "level": 2,
                "user": sub_child.name.username,
            }
            children.append(child_data)
        binarytree["children"] = children
        descendants.append(binarytree)
    return descendants


class GetMYParentandChildren(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = self.request.user
        x = MLMMember.objects.get(user=user)
        y = MLMBinary.objects.get(name=user)
        descendants_binary = get_descendants_up_to_2_levels(y, user)
        enrollment_tree_user = []
        for users in x.get_children():
            enrollment_tree_user.append({"username": users.user.username})
        return Response(
            {
                "message": "fetched tree of user",
                "data": {
                    "binary_tree": descendants_binary,
                    "enrollment_tree": enrollment_tree_user,
                },
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
