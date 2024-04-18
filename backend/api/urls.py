from django.urls import include, path
from rest_framework import routers

from .views import (
    PostViewSet,
    CommentViewSet,
    myposts,
)

app_name = 'api'

router_blog_v1 = routers.DefaultRouter()

router_blog_v1.register('posts', PostViewSet, basename='post')
router_blog_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router_blog_v1.urls)),
    path('', include('djoser.urls')),
    path('myposts/', myposts),
    path('auth/', include('djoser.urls.jwt')),
]