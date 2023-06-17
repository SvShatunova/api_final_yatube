from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите название группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес для страницы с группой',
        help_text='Адрес заполняется автоматически',
    )
    description = models.TextField(
        max_length=200,
        verbose_name='Описание',
        help_text='Укажите описание группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст сообщения',
        help_text='Введите текст сообщения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации сообщения',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор, к которому будет относится сообщение',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относится сообщение',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите файл',
        upload_to='posts/',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('id',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Напишите комментарий',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Текст комментария',
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите текст коментария',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания комментария',
        help_text='Дата написания комментария',
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('id',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',)
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан',)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.title
