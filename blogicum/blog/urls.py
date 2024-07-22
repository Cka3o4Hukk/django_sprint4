from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='create_post'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', views.PostEditView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
]

#handler403 = 'core.views.csrf_failure'
#handler404 = 'core.views.page_not_found'
#handler500 = 'core.views.server_error'
