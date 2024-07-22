from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm




@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostEditView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class Profile(ListView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    context_object_name = 'profile'
    slug_url_kward = 'username'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        


def index(request):
    posts = Post.objects.published()[:settings.POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'page_obj': posts})


def post_detail(request, post_id):
    posts = get_object_or_404(Post.objects.published(), id=post_id)
    return render(request, 'blog/detail.html', {'post': posts})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = category.posts.published()

    return render(request, 'blog/category.html',
                  {'post_list': post_list, 'category': category})
