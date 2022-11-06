import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.utils.decorators import auth, log_action, tryexcept
from core.utils.exceptions import TokenObtainException, KeycloakResponseException
from core.utils.http import Response
from core.utils.notification import telegram_message
from iam.keycloak import Keycloak
from iam.models import Impersonation
from settings.settings import FRONT_LOGIN_URL, KEYCLOAK_COOKIE_PATH, KEYCLOAK_COOKIE_EXPIRES_MIN
from users.models import User

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class ImpersonateUserView(APIView):
    keycloak = None

    def process_cookies(self, cookies):
        for key, value in cookies.items():
            if key == "KEYCLOAK_IDENTITY":
                cookies[key] = {
                    "value": value,
                    "secure": True,
                    "httponly": True,
                    "same_site": "None",
                    "expires_min": None,
                    "path": KEYCLOAK_COOKIE_PATH
                }
            elif key == "KEYCLOAK_IDENTITY_LEGACY":
                cookies[key] = {
                    "value": value,
                    "secure": True,
                    "httponly": True,
                    "same_site": "None",
                    "expires_min": None,
                    "path": KEYCLOAK_COOKIE_PATH
                }
            elif key == "KEYCLOAK_SESSION":
                cookies[key] = {
                    "value": value,
                    "secure": True,
                    "httponly": False,
                    "same_site": "None",
                    "expires_min": KEYCLOAK_COOKIE_EXPIRES_MIN,
                    "path": KEYCLOAK_COOKIE_PATH
                }
            elif key == "KEYCLOAK_SESSION_LEGACY":
                cookies[key] = {
                    "value": value, "secure": True,
                    "httponly": False,
                    "same_site": "None",
                    "expires_min": KEYCLOAK_COOKIE_EXPIRES_MIN,
                    "path": KEYCLOAK_COOKIE_PATH
                }
            else:
                cookies[key] = {
                    "value": value,
                    "secure": True
                }
        return cookies

    def dispatch(self, request, *args, **kwargs):
        try:
            self.keycloak = Keycloak()
        except TokenObtainException as error:
            return Response(status=400, content=error.message)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_uuid, *args, **kwargs):
        request_user = kwargs['user']
        try:
            target_user = User.objects.get(id=user_uuid)
        except ObjectDoesNotExist:
            return Response(status=400, content="Пользователь не найден")

        try:
            parsed_response, cookies = self.keycloak.impersonate_user(user_id=target_user.id)
        except KeycloakResponseException as error:
            message = f"Не удалось получить токен для входа от имени пользователя {target_user.id}. Ошибка {error}"
            telegram_message(message)
            logger.warning(message)
            return Response(status=400,
                            content="Не удалось получить токен для входа от имени другого пользователя, попробуйте повторить позднее")

        cookies = self.process_cookies(cookies)

        valid_until = timezone.now() + datetime.timedelta(minutes=30)
        token = Impersonation.generate_token(64)
        impersonation = Impersonation.objects.create(
            request_user=request_user,
            target_user=target_user,
            cookies=cookies,
            valid_until=valid_until,
            token=token)

        content = {"url": impersonation.get_impersonation_url(), "valid_until": str(impersonation.valid_until)}
        return Response(status=200, content=content)


@method_decorator([tryexcept, log_action], name='dispatch')
class ImpersonateUserLinkView(APIView):
    keycloak = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.keycloak = Keycloak()
        except TokenObtainException as error:
            return Response(status=400, content=error.message)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        try:
            impersonation = Impersonation.objects.get(token=token)
        except ObjectDoesNotExist:
            return Response(status=400, content="Токен невалиден")

        if impersonation.valid_until < timezone.now():
            return Response(status=400, content="Токен просрочен")

        headers = {"Location": FRONT_LOGIN_URL, "Content-Type": "application/json"}

        return Response(status=302,
                        headers=headers,
                        cookies=impersonation.cookies)
