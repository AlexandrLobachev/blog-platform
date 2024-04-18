from django.contrib.auth import get_user_model
from django.db import models

from blog import settings
from .querysets import PostQuerySet

User = get_user_model()


class Post(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200
    )
    text = models.TextField(verbose_name='Содержание')
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        help_text=('Если установить дату в будущем — можно делать '
                   'отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=200,
        choices = settings.POST_STATUS,
        blank=False,
        default='draft'
    )
    objects = PostQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title',
            )
        ]
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
