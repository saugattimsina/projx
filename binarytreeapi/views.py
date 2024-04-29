from django.shortcuts import render
from binarytree.models import MLMBinary, MLMMember, UserRank, MLMRank
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, permissions
from user.models import User
from subscription.models import UserSubcription
from .serializers import MLMRankSerializer


# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from utils.custom_response import SuccessResponse, FailedResponse


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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            x = MLMMember.objects.get(user=user)
            y = MLMBinary.objects.get(name=user)
            descendants_binary = get_descendants_up_to_2_levels(y)
            enrollment_tree_user = [
                {
                    "user": child.user.username,
                    "user_id": child.user.id,
                    "user_rank": UserRank.objects.get(
                        user=child.user
                    ).rank.equivalent_name,
                    "user_rank_image": UserRank.objects.get(
                        user=child.user
                    ).rank.rank_image.url,
                }
                for child in x.get_children()
            ]
            return SuccessResponse(
                message="Fetched tree of user",
                data={
                    "binary_tree": descendants_binary,
                    "enrollment_tree": enrollment_tree_user,
                },
            )
        except Exception as e:
            return FailedResponse(message=str(e))


class GetUserRankApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_rank = UserRank.objects.get(user=user)
            mlm_member = MLMMember.objects.get(user=user)
            mlm_binary = MLMBinary.objects.get(name=user)

            user_rank_level = user_rank.rank.rank_level
            user_direct_referrals = mlm_member.get_children_count()
            user_active_members = mlm_binary.get_descendant_count()

            if user_rank_level > 1:
                previous_rank = MLMRank.objects.filter(
                    rank_level=user_rank_level - 1
                ).first()
                previous_rank_serializer = (
                    MLMRankSerializer(previous_rank).data if previous_rank else None
                )
            else:
                previous_rank_serializer = None

            if user_rank_level < 6:
                next_rank = MLMRank.objects.filter(
                    rank_level=user_rank_level + 1
                ).first()
                next_rank_serializer = (
                    MLMRankSerializer(next_rank).data if next_rank else None
                )
            else:
                next_rank_serializer = None

            current_rank_serializer = MLMRankSerializer(user_rank.rank).data
            all_ranks = MLMRank.objects.all()
            all_rank_serializers = MLMRankSerializer(all_ranks, many=True)
            return Response(
                {
                    "current_rank": current_rank_serializer,
                    "previous_rank": previous_rank_serializer,
                    "next_rank": next_rank_serializer,
                    "current_user_stats": {
                        "user_direct_referrals": user_direct_referrals,
                        "user_active_members": user_active_members,
                    },
                    "all_ranks": all_rank_serializers.data,
                }
            )

        except UserRank.DoesNotExist:
            return Response(
                {"error": "UserRank not found for the given user.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MLMMember.DoesNotExist:
            return Response(
                {"error": "MLMMember not found for the given user.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MLMBinary.DoesNotExist:
            return Response(
                {"error": "MLMBinary not found for the given user.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )
