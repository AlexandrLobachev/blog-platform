import datetime

from django.db import models


class PostQuerySet(models.QuerySet):

    def published_post(self):
        """Фильтрует посты status = published и дата менее текущей."""
        return self.filter(status='published',
                           pub_date__lte=datetime.datetime.now())
