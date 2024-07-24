from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_available_posts(
    posts=Post.objects,
    filter_published=True,
    selected_related=True,
    comment_count=True
):
    if selected_related:
        posts = posts.select_related(
            'location',
            'author',
            'category',
        )
    if comment_count:
        posts = posts.annotate(comment_count=Count('comments')).order_by(
            *posts.model._meta.ordering
        )
    if filter_published:
        posts = posts.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    return posts
