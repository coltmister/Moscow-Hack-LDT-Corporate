import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.utils.decorators import auth, log_action, tryexcept
from core.utils.exceptions import TokenObtainException, KeycloakResponseException
from core.utils.http import Response
from core.utils.notification import telegram_message
from iam.keycloak import Keycloak
from users.models import User

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UpdatePasswordViaEmailView(APIView):
    keycloak = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.keycloak = Keycloak()
        except TokenObtainException as error:
            return Response(status=400, content=error.message)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Обновить пароль пользователя, отослав ссылку для смены пароля на основной email."""
        user_id = kwargs['user_id']
        userinfo = kwargs['userinfo']
        email = userinfo.get('email')
        hidden_email = f"{email[0]}***@***{email[-1]}" if email else "*****"

        try:
            self.keycloak.execute_actions_via_email(user_id=user_id, actions=['UPDATE_PASSWORD'])
            return Response(f"Письмо для сброса пароля было отправлено на адрес {hidden_email}")
        except KeycloakResponseException as error:
            message = f"Письмо для сброса пароля пользователя {user_id} не было отправлено. Ошибка {error}"
            logger.warning(message)
            telegram_message(message)
            return Response(
                content="Произошла ошибка, письмо для сброса пароля не было отправлено. Повторите попытку позже",
                status=400)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class ChangeUserActivityStatusView(APIView):
    keycloak = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.keycloak = Keycloak()
        except TokenObtainException as error:
            return Response(status=400, content=error.message)
        return super().dispatch(request, *args, **kwargs)

    def put(self, request, user_uuid, *args, **kwargs):
        """Заблокировать/разблокировать пользователя."""

        current_user = self.kwargs.get('user')
        if not current_user.is_admin:
            return Response(content="Вы не являетесь администратором", status=400)

        if current_user.id == user_uuid:
            return Response(content="Нельзя изменить свой статус активности", status=400)

        enabled = request.data.get('enabled')
        if enabled is None:
            return Response(status=400, content="Не указан параметр enabled")

        try:
            target_user = User.objects.get(id=user_uuid)
        except ObjectDoesNotExist:
            return Response(status=400, content=f"Пользователь не найден")

        attributes = {"enabled": enabled}

        try:
            self.keycloak.change_user_status(user_id=target_user.id, attributes=attributes)
        except KeycloakResponseException as error:
            message = f"Не удалось заблокировать пользователя {target_user.id}. Ошибка {error}"
            telegram_message(message)
            logger.warning(message)
            return Response(status=400,
                            content="Не удалось изменить статус активности пользователя, попробуйте повторить позднее")

        # Изменяю статус активности пользователя
        target_user.is_active = enabled
        target_user.save()

        return Response(status=204, content="Статус активности пользователя успешно изменен")
