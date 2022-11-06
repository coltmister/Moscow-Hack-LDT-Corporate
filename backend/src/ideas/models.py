import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import JSONField, CheckConstraint, Q, F

from core.models import AbstractBase
from users.models import User


# --- Модели для Идей ---
# models.CharField.register_lookup(search)
# models.TextField.register_lookup(search)


class Idea(AbstractBase):
    STATUS_CREATED = 'created'
    STATUS_ON_MODERATION = 'on_moderation'
    STATUS_NEED_WORK = 'need_work'
    STATUS_REJECTED = 'cancelled'
    STATUS_APPROVED = 'approved'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_ON_MODERATION, 'На модерации'),
        (STATUS_NEED_WORK, 'Нуждается в доработке'),
        (STATUS_REJECTED, 'Отклонена'),
        (STATUS_APPROVED, 'Одобрена'),
        (STATUS_FINISHED, 'Завершена'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    idea_json = JSONField(verbose_name='JSON идеи', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='ideas')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    category = models.ManyToManyField('IdeaCategory', verbose_name='Категории', related_name='ideas', blank=True)
    tags = models.ManyToManyField('users.Interest', verbose_name='Теги', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    subscribers = models.ManyToManyField(User, related_name='subscribe_ideas', verbose_name='Подписчики', blank=True)
    links = ArrayField(models.URLField(), blank=True, null=True, verbose_name='Ссылки')

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            IdeaSettings.objects.create(idea=self)
            IdeaInformation.objects.create(idea=self)
        return self

    def approve(self, message):
        self.status = self.STATUS_APPROVED
        IdeaStatusHistory.objects.create(idea=self, old_status=self.status, new_status=self.STATUS_APPROVED,
                                         comment=message)
        self.save()

    def reject(self, message):
        self.status = self.STATUS_REJECTED
        IdeaStatusHistory.objects.create(idea=self, old_status=self.status, new_status=self.STATUS_REJECTED,
                                         comment=message)
        self.save()

    def need_work(self, message):
        self.status = self.STATUS_NEED_WORK
        IdeaStatusHistory.objects.create(idea=self, old_status=self.status, new_status=self.STATUS_NEED_WORK,
                                         comment=message)
        self.save()

    def on_moderation(self, message):
        self.status = self.STATUS_ON_MODERATION
        IdeaStatusHistory.objects.create(idea=self, old_status=self.status, new_status=self.STATUS_ON_MODERATION,
                                         comment=message)
        self.save()

    def finished(self, message):
        self.status = self.STATUS_FINISHED
        IdeaStatusHistory.objects.create(idea=self, old_status=self.status, new_status=self.STATUS_FINISHED,
                                         comment=message)
        self.save()

    def __str__(self):
        return self.title

    def get_last_post(self):
        return self.posts.order_by('-created_at').first()

    class Meta:
        verbose_name = 'Идея'
        verbose_name_plural = 'Идеи'
        ordering = ['-created_at']


class IdeaStatusHistory(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name='Идея')
    old_status = models.CharField(max_length=255, verbose_name='Старый статус')
    new_status = models.CharField(max_length=255, verbose_name='Новый Статус')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def __str__(self):
        return f'{self.idea} - {self.old_status} -> {self.new_status}'

    class Meta:
        verbose_name = 'История статусов идеи'
        verbose_name_plural = 'История статусов идей'


class IdeaInformation(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='information')
    progress = models.IntegerField(default=0, verbose_name='Прогресс')
    budget = models.IntegerField(default=0, verbose_name='Бюджет')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.progress == 100:
            self.idea.status = self.idea.STATUS_FINISHED
            self.idea.save()
        return self


class Meta:
    verbose_name = 'Информация об идеи'
    verbose_name_plural = 'Информация об идеях'
    ordering = ['-created_at']


class IdeaComment(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='idea_comments')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Родительский комментарий', related_name='children')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий к идеи'
        verbose_name_plural = 'Комментарии к идеям'
        ordering = ['-created_at']
        constraints = [
            CheckConstraint(
                check=~Q(parent=F('id')),
                name='parent_row_not_equal_to_self'
            )]


class IdeaLike(AbstractBase):
    SUPER_LIKE = 'super_like'
    LIKE = 'like'
    NEUTRAL = 'neutral'
    DISLIKE = 'dislike'
    SUPER_DISLIKE = 'super_dislike'

    LIKES_CHOICES = (
        (SUPER_LIKE, "🥰"),
        (LIKE, "❤️"),
        (NEUTRAL, "😐"),
        (DISLIKE, "💔"),
        (SUPER_DISLIKE, "🤨"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    value = models.CharField(max_length=255, choices=LIKES_CHOICES, default='like', verbose_name='Значение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='likes')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='likes')

    def __str__(self):
        return self.idea.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.value == self.SUPER_LIKE:
            self.idea.rating += 2
        elif self.value == self.LIKE:
            self.idea.rating += 1
        elif self.value == self.DISLIKE:
            self.idea.rating -= 1
        elif self.value == self.SUPER_DISLIKE:
            self.idea.rating -= 2
        self.idea.save()

    def delete(self, *args, **kwargs):
        if self.value == self.SUPER_LIKE:
            self.idea.rating -= 2
        elif self.value == self.LIKE:
            self.idea.rating -= 1
        elif self.value == self.DISLIKE:
            self.idea.rating += 1
        elif self.value == self.SUPER_DISLIKE:
            self.idea.rating += 2
        self.idea.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['-created_at']


class IdeaCategory(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    idea_count = models.IntegerField(default=0, verbose_name='Количество идей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-created_at']


class IdeaSettings(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='settings')
    is_public = models.BooleanField(default=True, verbose_name='Публичная')
    is_commentable = models.BooleanField(default=True, verbose_name='Комментируемая')

    def __str__(self):
        return self.idea.title

    class Meta:
        verbose_name = 'Настройка идеи'
        verbose_name_plural = 'Настройки идеи'
        ordering = ['-created_at']


class IdeaDocument(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    path = models.CharField(max_length=255, verbose_name='Путь')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='documents')

    def __str__(self):
        return self.path

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-created_at']


# ------------------------------ Модели Постов ------------------------------

class Post(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name='Идея', related_name='posts')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    post_json = models.JSONField(verbose_name='JSON поста', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class PostLike(AbstractBase):
    SUPER_LIKE = 'super_like'
    LIKE = 'like'
    NEUTRAL = 'neutral'
    DISLIKE = 'dislike'
    SUPER_DISLIKE = 'super_dislike'

    LIKES_CHOICES = (
        (SUPER_LIKE, "🥰"),
        (LIKE, "❤️"),
        (NEUTRAL, "😐"),
        (DISLIKE, "💔"),
        (SUPER_DISLIKE, "🤨"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    value = models.CharField(max_length=255, choices=LIKES_CHOICES, default='like', verbose_name='Значение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='likes')

    def __str__(self):
        return self.post.title

    def save(self, *args, **kwargs):
        if self.value == self.SUPER_LIKE:
            self.post.rating += 2
        elif self.value == self.LIKE:
            self.post.rating += 1
        elif self.value == self.DISLIKE:
            self.post.rating -= 1
        elif self.value == self.SUPER_DISLIKE:
            self.post.rating -= 2
        self.post.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.value == self.SUPER_LIKE:
            self.post.rating -= 2
        elif self.value == self.LIKE:
            self.post.rating -= 1
        elif self.value == self.DISLIKE:
            self.post.rating += 1
        elif self.value == self.SUPER_DISLIKE:
            self.post.rating += 2
        self.post.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'
        ordering = ['-created_at']


class PostComment(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Родительский комментарий', related_name='children')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        constraints = [
            CheckConstraint(
                check=~Q(parent=F('id')),
                name='parent_row_not_equal_to_self_posts'
            )]


class PostDocument(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    path = models.CharField(max_length=255, verbose_name='Путь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='documents')

    def __str__(self):
        return self.path

    class Meta:
        verbose_name = 'Документ поста'
        verbose_name_plural = 'Документы постов'
        ordering = ['-created_at']
