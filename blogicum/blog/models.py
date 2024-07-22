from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = get_user_model()


class PublishedPostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PublishedPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


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
    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.',
    )
    image = models.ImageField(
        verbose_name='Изображение публикации',
        blank=True
    )
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

    class Meta(BaseBlogModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    objects = PostManager()

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]


class Comment(BaseBlogModel):
    text = models.TextField(
        verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    post = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост',
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        #ordering = ('created_at',)

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]
