from django_filters.rest_framework import (
    FilterSet,
    DateFilter,
)

from posts.models import Post


class PostFilter(FilterSet):
    pub_date = DateFilter('pub_date', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['status']