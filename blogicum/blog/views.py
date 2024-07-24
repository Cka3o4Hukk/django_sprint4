from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy


from .forms import PostForm, CommentForm
from .models import Post, Category
from .utils import (
    OnlyAuthorMixin, CommentEditMixin,
    BackToProfileMixin, get_available_posts)

# Посты


class Index(ListView):
    paginate_by = settings.PAGINATION
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_available_posts()


class PostCreateView(LoginRequiredMixin, BackToProfileMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditMixin:
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"


class PostEditView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.object.pk}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, PostEditMixin, DeleteView
):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.object), **kwargs
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', args=[self.request.user.username]
        )


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        post = super().get_object()
        if post.author == self.request.user:
            return post

        return get_object_or_404(
            get_available_posts(selected_related=False, comment_count=False),
            id=post.id
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            form=CommentForm(),
            comments=self.object.comments.select_related('author'))

# Комментарии


class CommentCreateView(LoginRequiredMixin,
                        CommentEditMixin, PostEditMixin, CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post, id=self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, OnlyAuthorMixin,
                        CommentEditMixin, DeleteView):

    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'


class CommentUpdateView(LoginRequiredMixin, OnlyAuthorMixin,
                        CommentEditMixin, UpdateView):

    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

# Профиль


class Profile(ListView):
    template_name = 'blog/profile.html'
    paginate_by = settings.PAGINATION

    def get_queryset(self):
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return get_available_posts(
            filter_published=self.request.user != self.author,
            selected_related=False).filter(author=self.author.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfile(LoginRequiredMixin, BackToProfileMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self):
        return self.request.user


class CategoryView(ListView):

    template_name = 'blog/category.html'
    paginate_by = settings.PAGINATION

    def get_queryset(self):
        return (
            get_available_posts()
            .filter(category__slug=self.kwargs['category_slug'])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, is_published=True, slug=self.kwargs["category_slug"]
        )
        return context
