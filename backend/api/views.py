from django.shortcuts import get_object_or_404
from django_filters.utils import translate_validation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

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
        if self.request.user.is_authenticated:
            post = Post.objects.filter(
                author__exact=self.request.user
            ) | Post.objects.published_post()
            return post
        return Post.objects.published_post()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        return get_object_or_404(
            Post.objects.published_post(),
            id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
