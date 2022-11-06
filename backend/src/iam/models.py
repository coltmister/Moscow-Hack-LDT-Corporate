import secrets
import uuid

from django.db import models

from core.models import AbstractBase
from iam.exceptions import TokenGenerationError
from settings.settings import END_SESSION_ENDPOINT, IMPERSONATION_URL


class LogoutUser(AbstractBase):
    """Таблица пользователей, которых необходимо вывести из системы"""
    REFRESH_TOKEN = 0
    LOGOUT = 1
    LOGOUT_TYPE = [
        (REFRESH_TOKEN, 'Обновление токена'),
        (LOGOUT, 'Выход из системы'),
    ]
    id = models.AutoField(primary_key=True, verbose_name="ID")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Пользователь")
    session_id = models.UUIDField(verbose_name="ID сессии", null=True, blank=True)
    iat_before = models.DateTimeField(verbose_name="Время выхода из системы")
    logout_type = models.IntegerField(choices=LOGOUT_TYPE, verbose_name="Тип выхода из системы", default=REFRESH_TOKEN)

    class Meta:
        verbose_name = "Logout пользователь"
        verbose_name_plural = "Logout пользователи"
        indexes = [
            models.Index(fields=['user', 'iat_before', 'logout_type']),
            models.Index(fields=['user', 'session_id']),
        ]

    def __str__(self):
        return f"{self.id} {self.user.id} {self.session_id} {self.iat_before} {self.logout_type}"


class VerifyCode(AbstractBase):
    """Таблица верификационных кодов."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', verbose_name="Пользователь", on_delete=models.CASCADE)
    code = models.CharField(verbose_name="Верификационный код", max_length=1024, null=True, blank=True,
                            default=uuid.uuid4, unique=True)
    value = models.CharField(verbose_name="Значение", max_length=1024, null=True, blank=True)
    is_used = models.BooleanField(verbose_name="Код использован?", default=False)
    use_until = models.DateTimeField(verbose_name="Код действителен до", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Верификационные коды"
        db_table = "VerifyCode"


class Impersonation(AbstractBase):
    id = models.AutoField(primary_key=True)
    request_user = models.ForeignKey('users.User', verbose_name="Автор запроса", on_delete=models.CASCADE,
                                     related_name="request_user")
    target_user = models.ForeignKey('users.User', verbose_name="Целевой пользователь", on_delete=models.CASCADE,
                                    related_name="target_user")
    cookies = models.JSONField(verbose_name="Cookies")
    valid_until = models.DateTimeField(verbose_name="Действителен до")
    token = models.CharField(verbose_name="Токен", max_length=1024, unique=True)

    class Meta:
        verbose_name_plural = "Impersonation"
        db_table = "Impersonation"

    @staticmethod
    def generate_token(token_length=1024):
        if token_length > 1024:
            raise TokenGenerationError("Длина токена не может быть больше 1024")

        token = secrets.token_urlsafe(64)
        while Impersonation.objects.filter(token=token).exists():
            token = secrets.token_urlsafe(64)
        return token

    def get_impersonation_url(self):
        return f"{END_SESSION_ENDPOINT}?post_logout_redirect_uri={IMPERSONATION_URL}?token={self.token}"
