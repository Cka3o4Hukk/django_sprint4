from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Location, Post, User


admin.site.unregister(User)
# Отмена регистрации встроенной модели пользователя
admin.site.register(User, UserAdmin)
# Регистрация пользовательской модели с использованием UserAdmin


@admin.register(Post)  # первый способ
class PostAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = (
        'id', 'title', 'author', 'text', 'category',
        'pub_date', 'location', 'is_published', 'created_at',
    )
    link_display_links = ('title',)
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('description', )
    list_display = (
        'id', 'title', 'description', 'created_at', 'is_published', 'slug'
    )
    list_editable = ('title', 'is_published')
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'is_published'
    )
    search_fields = ('name', )
