import uuid

from django.db import models

from core.models import AbstractBase
from users.models import TeamRole, User


class RequiredMembers(AbstractBase):
    team = models.ForeignKey('teams.Team',
                             on_delete=models.CASCADE,
                             verbose_name='Команда')
    role = models.ForeignKey('users.TeamRole',
                             on_delete=models.CASCADE,
                             verbose_name="Роль в команде")
    amount = models.IntegerField(verbose_name="Количество людей с данной ролью", default=1)

    def __str__(self):
        return f'{self.team} - {self.role} - {self.amount}'
    class Meta:
        verbose_name = "Требуемые роли в команде"
        verbose_name_plural = "Требуемые роли в команде"
        constraints = [
            models.UniqueConstraint(fields=['role', 'team'], name="team_role_unique")
        ]
        ordering = ['-created_at']


class Team(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Команды")
    name = models.CharField(max_length=255, verbose_name="Название команды", unique=True)
    description = models.TextField(verbose_name="Описание команды", null=True, blank=True)
    idea = models.OneToOneField('ideas.Idea',
                                on_delete=models.CASCADE,
                                verbose_name="Идея", related_name="team")
    members = models.ManyToManyField('users.User',
                                     verbose_name="Участники команды",
                                     related_name='teams',
                                     through='Membership',
                                     through_fields=('team', 'user'))
    team_leader = models.ForeignKey('users.User',
                                    verbose_name="Лидер команды",
                                    related_name='team_leader',
                                    on_delete=models.CASCADE)
    is_looking_for_members = models.BooleanField(default=True, verbose_name="Ищет ли команда участников?")
    required_members = models.ManyToManyField('users.TeamRole',
                                              verbose_name="Необходимые участники",
                                              related_name='required_roles',
                                              through='RequiredMembers')
    chat = models.OneToOneField('chats.Chat',
                                on_delete=models.SET_NULL,
                                verbose_name="Чат команды",
                                null=True,
                                blank=True,
                                related_name='team_chat')

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}. 🌝 {self.name}"


class Membership(AbstractBase):
    AUTOMATIC = 0
    USER = 1
    TEAM = 2
    ADMINISTRATOR = 3

    MEMBERSHIP_INITIATOR = (
        (AUTOMATIC, 'Автоматически'),
        (USER, 'Пользователь'),
        (TEAM, 'Команда'),
        (ADMINISTRATOR, 'Администратор'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Дата вступления")
    membership_requester = models.IntegerField(choices=MEMBERSHIP_INITIATOR, verbose_name="Инициатор членства")
    role = models.ForeignKey(TeamRole, on_delete=models.CASCADE, verbose_name="Роль в команде", null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.team} - {self.date_joined} - {self.role}'
    class Meta:
        verbose_name = "Членство в команде"
        verbose_name_plural = "Членство в команде"
        constraints = [
            models.UniqueConstraint(fields=['user', 'team'], name="user_team_unique")
        ]
        ordering = ['-created_at']


class TeamRequest(AbstractBase):
    INCOMING = 0
    OUTGOING = 1

    REQUEST_TYPE = (
        (INCOMING, 'Входящий запрос'),
        (OUTGOING, 'Исходящий запрос'),
    )

    REQUEST_SUBMITTED = 0
    REQUEST_ACCEPTED = 1
    REQUEST_DECLINED = 2

    REQUEST_STATUS = (
        (REQUEST_SUBMITTED, 'Подана'),
        (REQUEST_ACCEPTED, 'Принята'),
        (REQUEST_DECLINED, 'Отклонена'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Заявки")
    team = models.ForeignKey(Team, verbose_name="Команда", related_name='team_requests', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', verbose_name="Пользователь", related_name='user_requests',
                             on_delete=models.CASCADE)
    role = models.ForeignKey(TeamRole, on_delete=models.CASCADE, verbose_name="Роль пользователя",
                             related_name='user_role_requests')
    request_type = models.PositiveSmallIntegerField(choices=REQUEST_TYPE, verbose_name="Тип запроса")
    cover_letter = models.TextField(verbose_name="Сопроводительное письмо", null=True, blank=True)
    request_status = models.IntegerField(verbose_name="Статус запроса", default=REQUEST_SUBMITTED,
                                         choices=REQUEST_STATUS)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}. 🌝 {self.team} {self.user} {self.request_type} {self.request_status}"
