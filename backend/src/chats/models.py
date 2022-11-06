import uuid
import random

from django.db import models

from core.models import AbstractBase


class Chat(AbstractBase):
    TEAM_CHAT = 0
    INTEREST_CHAT = 1

    CHAT_TYPE = (
        (TEAM_CHAT, 'Чат команды'),
        (INTEREST_CHAT, 'Чат по интересам'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID чата")
    name = models.CharField(max_length=255, verbose_name="Название чата")
    chat_link = models.URLField(verbose_name="Ссылка на чат вк")
    chat_id = models.IntegerField(verbose_name="ID чата вк", unique=True)
    peer_id = models.IntegerField(verbose_name="Peer ID чата вк", unique=True)
    users_count = models.IntegerField(verbose_name="Количество пользователей в чате", default=0)
    chat_type = models.IntegerField(choices=CHAT_TYPE, verbose_name="Тип чата", default=TEAM_CHAT)

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}. 🌝 {self.name}"

    def get_team_chat_init_greeting_message(self, user_first_name):
        if not self.chat_type == Chat.TEAM_CHAT:
            return f"Привет, {user_first_name}! Добро пожаловать в чат '{self.name}'. "

        if self.team_chat.members.all().count() > 1:
            message = f"""Привет, {user_first_name}! Добро Пожаловать в чат команды '{self.team_chat.name}'." \
                          Мы видим, что в вашей команде уже есть участники. Половина дела сделана!
                          Им всем мы уже прислали уведомления. Ожидайте, пока они присоединятся.
                          В этот чат будут приходить важные уведомления как от команды, так и от администрации.
                          
                          С ❤️, Агенство Инноваций Москвы."""
        else:
            message = f"""Привет, {user_first_name}! Добро Пожаловать в чат команды '{self.team_chat.name}'." \
                          В вашей команде пока что нет участников, но вы всегда можете пригласить их на портале.
                          Успехов в реализации идей!
                          
                          С ❤️, Агенство Инноваций Москвы."""
        return message

    def get_new_person_joined(self, user_first_name):
        message = f"Привет, {user_first_name}! Добро пожаловать в чат команды '{self.team_chat.name}'." \
                  f"Представься и расскажи, пожалуйста, немного о себе, чтобы другие участники команды могли лучше тебя узнать. "

        return message

    def get_kicked_user_message(self):
        message = f"Расскажите, почему вы исключили данного пользователя? Он не подошел команде? " \
                  f"Администрация использует эту информацию для более качественного дальнейшего подбора участников. "

        return message

    @staticmethod
    def get_tag_message(is_question=False):
        affirmative_answers = ["Привет! Уже передаю ваше сообщение администратору, он ответит в ближайшее время",
                               "Привет! Рады, что вы обращаетесь к нам! Передадим запрос администратору",
                               "Привет! Спасибо, что обратились к нам! Передадим запрос администратору"]

        question_answers = ["Привет! Спасибо за вопрос! Передадим его администратору",
                            "Привет! Ваш вопрос будет передан администратору. Спасибо за обращение.",
                            "Уже отправили оповещение администратору. Он скоро ответит.",
                            "Спасибо, что обратились к нам! Передадим запрос администратору"]
        if is_question:
            return random.choice(question_answers)
        else:
            return random.choice(affirmative_answers)


class ChatNotification(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID чата")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="Чат")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    class Meta:
        verbose_name = "Уведомления в чатах"
        verbose_name_plural = "Уведомления в чатах"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}. 🌝 {self.message}"
