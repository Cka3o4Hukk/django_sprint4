from django.db import models
from django.utils.timezone import now
from django.db.models import Count


class PublishedPostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True)

    def annotate_comments(self):
        return self.annotate(
            comment_count=Count('comments')).order_by('-pub_date')

# я не могу обратиться к модели Post тк из-за from django.db import models
# возникает ошибка, поэтому я прописываю order_by
# пробовал через Post = apps.get_model('Post'), но тоже безуспешно
