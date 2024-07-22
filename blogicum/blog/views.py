from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, DeleteView
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


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
   # success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')





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
