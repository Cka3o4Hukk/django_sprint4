from django.db import models
from django.utils.timezone import now


class PublishedPostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True)
