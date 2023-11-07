from django.shortcuts import render
from binarytree.models import MLMBinary, MLMMember, UserRank, MLMRank
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from subscription.models import UserSubcription


# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


def get_descendants_up_to_2_levels(node):
    descendants = []

    def build_descendant_tree(node, level):
        descendant = {
            "level": level,
            "user_id": node.name.id,
            "user": node.name.username,
            "user_rank": UserRank.objects.get(user=node.name).rank.equivalent_name,
            "user_rank_image": UserRank.objects.get(user=node.name).rank.rank_image.url,
            "children": [],
        }
        if level < 2:
            for child in node.get_children():
                descendant["children"].append(build_descendant_tree(child, level + 1))
        return descendant

    descendants = build_descendant_tree(node, level=0)
    return descendants


class GetMYParentandChildren(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found", "success": False}, status=404)
        x = MLMMember.objects.get(user=user)
        y = MLMBinary.objects.get(name=user)
        descendants_binary = get_descendants_up_to_2_levels(y)
        enrollment_tree_user = [
            {
                "user": child.user.username,
                "user_id": child.user.id,
                "user_rank": UserRank.objects.get(user=child.user).rank.equivalent_name,
                "user_rank_image": UserRank.objects.get(
                    user=child.user
                ).rank.rank_image.url,
            }
            for child in x.get_children()
        ]

        return Response(
            {
                "message": "Fetched tree of user",
                "data": {
                    "binary_tree": descendants_binary,
                    "enrollment_tree": enrollment_tree_user,
                },
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


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
                    if required_refferals < 0:
                        required_refferals = 0
                if team_size < next_rank.min_team_size:
                    required_team_size = next_rank.min_team_size - team_size
                    if required_team_size < 0:
                        required_team_size = 0
            return Response(
                {
                    "message": "User rank and requirement for next rank fetched successfully",
                    "data": {
                        "current_rank": {
                            "name": user_rank.rank.equivalent_name
                            if user_rank
                            else None,
                            "image": user_rank.rank.rank_image.url
                            if user_rank.rank.rank_image
                            else None,
                            "total_referal": referrals,
                            "team_size": team_size,
                        },
                        "previous_rank": {
                            "name": previous_rank.equivalent_name
                            if previous_rank
                            else None,
                            "image": previous_rank.rank_image.url
                            if previous_rank
                            else None,
                        },
                        "next_rank": {
                            "name": next_rank.equivalent_name if next_rank else None,
                            "image": next_rank.rank_image.url if next_rank else None,
                            "total_numbers_of_referal": next_rank.min_referrals
                            if next_rank
                            else None,
                            "total_team_size": next_rank.min_team_size
                            if next_rank
                            else None,
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
