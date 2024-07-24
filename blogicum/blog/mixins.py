from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().pk)


class CommentEditMixin:
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class BackToProfileMixin:
    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostEditMixin:
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'


class CommentPkMixin:
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
