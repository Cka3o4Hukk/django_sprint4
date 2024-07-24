from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from .published_post import PublishedPostQuerySet
User = get_user_model()


class BaseBlogModel(models.Model):

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')

    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created_at', )


class Category(BaseBlogModel):
    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]


class Location(BaseBlogModel):
    name = models.CharField('Название места',
                            max_length=settings.MAX_FIELD_LENGTH)

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:settings.REPRESENTATION_LENGTH]


class Post(BaseBlogModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    location = models.ForeignKey(
        Location,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )

    image = models.ImageField(
        verbose_name='Изображение публикации',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.',
    )
    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    text = models.TextField('Текст')

    objects = PublishedPostQuerySet.as_manager()

    class Meta(BaseBlogModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    text = models.TextField(
        max_length=500,
        verbose_name="Текст комментария",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)
        default_related_name = "comments"

    def __str__(self):
        return self.text
