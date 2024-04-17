from ..apiview import create_new_history
from ..models import TradeHistory
from ..filters.trade_history_filter import TradeHistoryFilter
from ..serializers import TradesHistorySerializer
from ..services import create_user_new_history

from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class TradeHistroyApiViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TradesHistorySerializer
    queryset = TradeHistory.objects.all()
    filterset_class = TradeHistoryFilter

    def get_queryset(self):
        user = self.request.user
        queryset = TradeHistory.objects.filter(user=user).order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):
        user = request.user
        create_user_new_history(user=user)
        return super().list(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     try:
    #         user = request.user
    #         create_user_new_history(user=user)
    #         queryset = TradeHistory.objects.filter(user=user)
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             return self.get_paginated_response(serializer.data)

    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(
    #             {
    #                 "message": "user history fetched",
    #                 "data": serializer.data,
    #                 "success": True,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as e:
    #         return Response(
    #             {"message": str(e), "success": False},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
