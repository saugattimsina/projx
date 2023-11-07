from django.shortcuts import render
from binarytree.models import MLMBinary, MLMMember, UserRank, MLMRank
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from subscription.models import UserSubcription


# Create your views here.
def get_descendants_up_to_2_levels(node, parent):
    descendants = []

    binarytree = {}  # Create a dictionary for the parent
    binarytree["parent"] = parent
    binarytree["left_children"] = []
    binarytree["right_children"] = []
    count = 0
    inner_count = 0
    for child in node.get_children():
        child_data = {
            "level": 1,
            "user": child.name.username,
            "user_rank": UserRank.objects.get(user=child.name).rank.equivalent_name,
            "user_rank_image": UserRank.objects.get(user=child.name).rank.rank_image.path,           
            "left_children": [],
            "right_children": [],
        }

        for sub_child in child.get_children():
            sub_child_data = {"level": 2, "user": sub_child.name.username, "user_rank": UserRank.objects.get(user=sub_child.name).rank.equivalent_name,"user_rank_image": UserRank.objects.get(user=sub_child.name).rank.rank_image.path}
            if inner_count == 0:
                child_data["left_children"].append(sub_child_data)
                inner_count = inner_count + 1
            else:
                child_data["right_children"].append(sub_child_data)
                inner_count = 0

        if count == 0:
            binarytree["left_children"].append(child_data)
            count = count + 1
        else:
            binarytree["right_children"].append(child_data)
            count = 0

    descendants.append(binarytree)
    return descendants


class GetMYParentandChildren(APIView):
    # authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            try:
                mlm_user = MLMBinary.objects.get(name=user)
                try:
                    x = mlm_user.get_parent()
                    parent = x.name.username
                except:
                    x = mlm_user
                    parent = mlm_user.name.username
                print(x, parent)
                binary_tree = get_descendants_up_to_2_levels(x, parent)
                enrollment_tree_user = []
                y = MLMMember.objects.get(user=user)
                for users in y.get_children():
                    user_sub = UserSubcription.objects.filter(user=users.user).first()
                    if user_sub.plan.package_type == "free":
                        date = "unknown"
                    else:
                        date = user_sub.end_date
                    enrollment_tree_user.append(
                        {"user": users.user.username, "user_rank": UserRank.objects.get(user=users.user).rank.equivalent_name, "user_rank_image": UserRank.objects.get(user=users.user).rank.rank_image.path, "expire_date": date}
                    )
                return Response(
                    {
                        "message": "fetched tree of user",
                        "data": {
                            "binary_tree": binary_tree,
                            "enrollment_tree": enrollment_tree_user,
                        },
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            except MLMBinary.DoesNotExist:
                return Response(
                    {"error": "User not found", "success": False}, status=404
                )
        except User.DoesNotExist:
            return Response({"error": "User not found", "success": False}, status=404)


class GetUserRankApiView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user_rank = UserRank.objects.get(user=user)
            next_rank = (
                MLMRank.objects.filter(min_referrals__gt=user_rank.rank.min_referrals)
                .order_by("min_referrals")
                .first()
            )
            previous_rank = (
                MLMRank.objects.filter(min_referrals__lt=user_rank.rank.min_referrals)
                .order_by("-min_referrals")
                .first()
            )
            x = MLMMember.objects.get(user=user)
            referrals = x.get_children_count()
            team_size = x.get_descendant_count()
            required_refferals = 0
            required_team_size = 0
            if next_rank:
                if referrals < next_rank.min_referrals:
                    required_refferals = next_rank.min_referrals - referrals
                    if required_refferals <0 :
                        required_refferals = 0
                elif team_size < next_rank.min_team_size:
                    required_team_size = next_rank.min_team_size - team_size
                    if required_team_size <0 :
                        required_team_size = 0
            return Response(
                {
                    "message": "User rank and requirement for next rank fetched successfully",
                    "data": {
                        "current_rank":{

                            "user_rank": user_rank.rank.equivalent_name if user_rank else None,
                            "user_rank_image": user_rank.rank.rank_image.url if user_rank.rank.rank_image else None,
                            'total_referal' : referrals,
                            "team_size": team_size,
                        },
                        "previous_rank":
                        {
                            "name" : previous_rank.equivalent_name if previous_rank else None,
                            "image" : previous_rank.rank_image.url if previous_rank else None,

                        },
                        "next_rank":{
                            "name": next_rank.equivalent_name if next_rank else None,
                            "image": next_rank.rank_image.url if next_rank else None,
                            "total_numbers_of_referal": next_rank.min_referrals if next_rank else None,
                            "total_team_size": next_rank.min_team_size if next_rank else None,

                        },
                        "condition_for_next_rank": {
                            "required_direct_refferal": required_refferals,
                            "required_team_size": required_team_size,
                        },
                    },
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"error": "User not found", "success": False}, status=404)
