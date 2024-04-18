import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from posts.models import Post, Comment


class CommentSerializer(ModelSerializer):
    """Сериализатор для комментариев."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class PostSerializer(ModelSerializer):
    """Сериализатор для постов."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'status')
        model = Post

    def validate_pub_date(self, pub_date):
        if pub_date < datetime.date.today():
            raise ValidationError('Дата не может быть ранее текущей!')
        return pub_date
