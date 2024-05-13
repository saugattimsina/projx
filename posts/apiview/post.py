from django.shortcuts import render

# Create your views here.
from ..models import Post
from ..serializers import PostSerializers
from ..filters import PostFilter

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    filterset_class = PostFilter

    @action(detail=False, methods=["get"])
    def published(self, request):
        """
        This action returns a list of all posts that are marked as 'PUBLISHED'.
        """
        published_posts = Post.objects.filter(status=Post.Status.PUBLISHED)
        page = self.paginate_queryset(published_posts)
        if page is not set:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)


class PublicPostViewSet(ReadOnlyModelViewSet):
    serializer_class = PostSerializers
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    filterset_class = PostFilter
