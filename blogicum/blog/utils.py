from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import Post, CommentForm
from .models import Post, Comment


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


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().pk)


class CommentEditMixin:
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class BackToProfileMixin:
    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )
