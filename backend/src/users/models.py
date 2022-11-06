import uuid

from django.db import models

from core.models import AbstractBase
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractBase):
    id = models.UUIDField(primary_key=True, verbose_name="ID Пользователя")
    username = models.CharField(max_length=255, verbose_name="Username пользователя", unique=True)
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия пользователя")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество пользователя", null=True, blank=True)
    email = models.EmailField(verbose_name="Адрес электронной почты пользователя", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Пользователь активен?")
    is_admin = models.BooleanField(default=False, verbose_name="Пользователь является администратором?")
    is_verified = models.BooleanField(default=False, verbose_name="Пользователь верифицирован?")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}. 🌝 {self.username} {self.surname} {self.name} {self.patronymic} {self.email} {self.is_active}"

    @property
    def snp(self):
        user_patronymic = self.patronymic or ""
        return f'{self.surname} {self.name} {user_patronymic}'.strip()

    @property
    def avatar(self):
        return self.profile.avatar

    @property
    def avatar_thumbnail(self):
        return self.profile.avatar_thumbnail

    def get_greeting_name(self):
        greeting_name = f"{self.name} {self.patronymic}" if self.patronymic else f"{self.name}"
        return greeting_name


class SocialNetwork(AbstractBase):
    """
    Таблица для хранения логинов и соц. сетей,
    стоит ограничение на логин+соц.сеть во избежание дубликатов
    """
    NETWORK_TYPE = [
        ('Вконтакте', 'Вконтакте'),
        ('Telegram', 'Telegram'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('YouTube', 'YouTube'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Google', 'Google'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID соц. сети")
    network_type = models.CharField(max_length=10, choices=NETWORK_TYPE, verbose_name='Тип соц.сети')
    nickname = models.CharField(max_length=120, verbose_name="Никнейм в соц. сети")
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name="Профиль пользователя",
                                     related_name='social_networks')

    class Meta:
        verbose_name = "Социальные сети"
        verbose_name_plural = "Социальные сети"
        constraints = [
            models.UniqueConstraint(fields=['network_type', 'nickname'], name='unique_social_network')
        ]

    def __str__(self):
        return f"[{self.id}] {self.user_profile.user.snp} -> {self.nickname}"


class ProfileSettings(AbstractBase):
    """
    Таблица с информацией о приватности каждого из пунктов
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID информации о приватности")
    show_birthdate = models.BooleanField(default=True, verbose_name="Показывать ДР?")
    show_sex = models.BooleanField(default=True, verbose_name="Показывать пол?")
    show_biography = models.BooleanField(default=True, verbose_name="Показывать биографию?")
    show_phone = models.BooleanField(default=False, verbose_name="Показывать осн. телефон?")
    show_email = models.BooleanField(default=False, verbose_name="Показывать осн. почту?")
    show_social_networks = models.BooleanField(default=True, verbose_name="Показывать соц. сети?")
    show_skills = models.BooleanField(default=True, verbose_name="Показывать навыки?")
    show_interests = models.BooleanField(default=True, verbose_name="Показывать интересы?")

    show_citizenship = models.BooleanField(default=True, verbose_name="Показывать гражданство?")
    show_education = models.BooleanField(default=True, verbose_name="Показывать образование?")
    show_employment = models.BooleanField(default=True, verbose_name="Показывать статус трудоустройства?")
    show_work_experience = models.BooleanField(default=True, verbose_name="Показывать опыт работы?")
    show_professional_experience = models.BooleanField(default=True, verbose_name="Показывать профессиональные навыки?")
    show_team_roles = models.BooleanField(default=True, verbose_name="Показывать роли в командах?")
    show_iar_information = models.BooleanField(default=True, verbose_name="Показывать информацию о РИД?")
    show_company_information = models.BooleanField(default=True, verbose_name="Показывать информацию о компании?")
    show_hack_experience = models.BooleanField(default=True, verbose_name="Показывать опыт участия в хакатонах?")

    can_be_invited = models.BooleanField(default=True, verbose_name="Может ли быть приглашен в группу?")

    class Meta:
        verbose_name = "Настройки профиля"
        verbose_name_plural = "Настройки профиля"

    def __str__(self):
        return f"[{self.id}] {self.profile}"


class Skill(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID навыка")
    name = models.CharField(max_length=255, verbose_name="Название навыка")
    weight = models.IntegerField(default=0, verbose_name="Вес навыка")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Родительский навык", null=True,
                               blank=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Interest(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID интереса")
    name = models.CharField(max_length=255, verbose_name="Название интереса")
    weight = models.IntegerField(default=0, verbose_name="Вес интереса")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Родительский интерес", null=True,
                               blank=True)
    chat = models.ForeignKey('chats.Chat', on_delete=models.CASCADE, verbose_name="Чат", related_name='interest',
                             null=True,
                             blank=True)

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def save(self, *args, **kwargs):
        from chats.views import create_interest_chat
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            create_interest_chat.apply_async(kwargs={"interest_pk": str(self.id)}, countdown=5)
        else:
            if not self.chat:
                create_interest_chat.apply_async(kwargs={"interest_pk": str(self.id)}, countdown=5)
        return self


class UserProfile(AbstractBase):
    """
    Основная таблица для хранения пользователя с основной информацией и доп. полями
    - Соц. сети
    - Телефоны
    - Почты
    - Родственники
    """
    MALE = 'male'
    FEMALE = 'female'
    SEX = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID информации о пользователе")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь",
                                related_name="profile")
    status = models.CharField(max_length=255, blank=True, null=True, verbose_name="Статус человека")
    avatar = models.URLField(max_length=2048, blank=True, null=True, verbose_name="Аватар")
    avatar_thumbnail = models.URLField(max_length=2048, blank=True,
                                       null=True, unique=True, verbose_name="Миниатюра аватара")
    biography = models.TextField(blank=True, null=True, verbose_name="Биография")

    phone = models.CharField(max_length=20, verbose_name="Номер телефона пользователя в международном формате",
                             unique=True, null=True, blank=True)
    birthdate = models.DateField(verbose_name="Дата рождения пользователя", null=True, blank=True)

    sex = models.CharField(max_length=10, verbose_name="Пол пользователя", choices=[('female', 'Жен'), ('male', 'Муж')],
                           null=True, blank=True)

    profile_settings = models.OneToOneField(ProfileSettings, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name="Какие поля показывать?", related_name="profile")
    skills = models.ManyToManyField(Skill, blank=True, verbose_name="Навыки пользователя")
    interests = models.ManyToManyField(Interest, blank=True, verbose_name="Интересы пользователя")

    class Meta:
        verbose_name = "Профили пользователей"
        verbose_name_plural = "Профиль пользователя"

    def save(self, *args, **kwargs):
        if self.profile_settings is None:
            self.profile_settings = ProfileSettings.objects.create()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.user}]"


class Country(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID страны")
    name = models.CharField(max_length=255, verbose_name="Название страны")
    country_code = models.CharField(max_length=255, verbose_name="Код страны")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return f"[{self.id}] {self.name}"


class University(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID университета")
    name = models.CharField(max_length=255, verbose_name="Название университета")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг университета")

    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"

    def __str__(self):
        return f"[{self.id}] {self.name}"


class TeamRole(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID роли")
    name = models.CharField(max_length=255, verbose_name="Название роли")
    weight = models.IntegerField(default=0, verbose_name="Вес роли")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return f"[{self.id}] {self.name}"


class UserAddInfo(AbstractBase):
    """
    Таблица дополнительной информации о пользователе
    """
    FULL = 0
    PART = 1
    PROJECT = 2
    VOLUNTEER = 3
    TRAINEE = 4
    BUSINESS = 5
    SELF_EMPLOYED = 6
    UNEMPLOYED = 7

    EMPLOYMENT = (
        (FULL, 'Полная занятость'),
        (PART, 'Частичная занятость'),
        (PROJECT, 'Проектная работа'),
        (VOLUNTEER, 'Волонтерство'),
        (TRAINEE, 'Стажировка'),
        (BUSINESS, 'Свой бизнес'),
        (SELF_EMPLOYED, 'Самозанятый'),
        (UNEMPLOYED, 'Безработный'),

    )

    BASIC_GENERAL_EDUCATION = 0
    SECONDARY_SCHOOL = 1
    LOWER_POST_SECONDARY_VOCATIONAL_EDUCATION = 2
    INCOMPLETE_HIGHER_EDUCATION = 3
    BACHELOR = 4
    SPECIALIST = 5
    MASTER = 6
    POSTGRADUATE = 7
    PHD = 8

    EDUCATION_LEVEL = (
        (BASIC_GENERAL_EDUCATION, 'Среднее общее образование (9 классов)'),
        (SECONDARY_SCHOOL, 'Среднее полное образование (11 классов)'),
        (LOWER_POST_SECONDARY_VOCATIONAL_EDUCATION, 'Среднее профессиональное образование'),
        (INCOMPLETE_HIGHER_EDUCATION, 'Незаконченное высшее образование'),
        (BACHELOR, 'Бакалавриат'),
        (SPECIALIST, 'Специалитет'),
        (MASTER, 'Магистратура'),
        (POSTGRADUATE, 'Аспирантура'),
        (PHD, 'Докторантура'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID заявки")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="add_info")
    citizenship = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name="Гражданство")
    education_university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True,
                                             verbose_name="Университет")
    education_level = models.IntegerField(default=BACHELOR, verbose_name="Уровень образования", choices=EDUCATION_LEVEL)
    education_speciality = models.CharField(max_length=255, blank=True, null=True, verbose_name="Специальность")
    education_end_year = models.IntegerField(blank=True, null=True, verbose_name="Год окончания обучения")
    employment = models.IntegerField(choices=EMPLOYMENT, default=FULL, blank=True, null=True, verbose_name="Занятость")
    work_experience = models.IntegerField(blank=True, null=True, verbose_name="Опыт работы",
                                          validators=[MaxValueValidator(60)])
    professional_experience = models.TextField(blank=True, null=True, verbose_name="Профессиональный опыт")
    team_role = models.ManyToManyField(TeamRole, blank=True, verbose_name="Роль в команде")
    has_iar = models.BooleanField(default=False, verbose_name="Наличие РИД")
    has_own_company = models.BooleanField(default=False, verbose_name="Наличие собственной компании")
    hack_experience = models.IntegerField(blank=True, null=True, verbose_name="Опыт участия в хакатонах",
                                          validators=[MaxValueValidator(60)])

    class Meta:
        verbose_name = "Доп. информация о пользователе"
        verbose_name_plural = "Доп. информация о пользователе"

    def __str__(self):
        return f"[{self.id}] {self.user}"
