from django.db.migrations import serializer
from django.shortcuts import render, get_object_or_404
from django_filters.utils import translate_validation
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from .filters import PostFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment
from blog.settings import PAGINATION_SIZE


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.published_post()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def myposts(self, request):
        queryset = self.filter_queryset(request.user.posts.all())
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def myposts(request):
    paginator = PageNumberPagination()
    paginator.page_size = PAGINATION_SIZE

    filterset = PostFilter(request.GET, queryset=request.user.posts.all())
    if not filterset.is_valid():
        raise translate_validation(filterset.errors)

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = PostSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
