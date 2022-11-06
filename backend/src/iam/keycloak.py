import json
import logging
import traceback
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

import requests
from django.utils import timezone
from requests import JSONDecodeError

from core.utils.exceptions import TokenObtainException, KeycloakResponseException
from core.utils.http import parse_response
from core.utils.notification import telegram_message
from settings.settings import CLIENT_SECRET, CLIENT_ID, AUTHORIZATION_ENDPOINT, ADMIN_URL, USERS_ENDPOINT, \
    ACCOUNT_SESSION_URL, ADMIN_SESSION_URL, USER_INFO_ENDPOINT

logger = logging.getLogger(__name__)


@dataclass
class Role():
    pass


class Keycloak:
    """Класс для взаимодействия с Keycloak"""

    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.access_token = self.obtain_service_account_access_token()

    @staticmethod
    def get_user_info(access_token):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f"Bearer {access_token}"}
        response = requests.request("POST", USER_INFO_ENDPOINT, headers=headers)
        return parse_response(response)

    def obtain_service_account_access_token(self) -> Optional[str]:
        """
        Метод получает токен сервисного аккаунта
        :return: access_token или None, если произошла ошибка
        """
        payload = f'client_secret={self.client_secret}&client_id={self.client_id}&grant_type=client_credentials'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", AUTHORIZATION_ENDPOINT, headers=headers, data=payload)
        try:
            access_token = response.json()['access_token']
        except (JSONDecodeError, KeyError):
            message = f'Не удалось получить сервисный access_token. Traceback: {traceback.format_exc()}'
            logger.warning(message)
            telegram_message(message)
            raise TokenObtainException("Не удалось получить сервисный токен авторизации")
        else:
            return access_token

    def get_user_data(self, user_id: UUID | str) -> (bool, dict):
        """Метод возвращает представление пользователя"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("GET", f"{USERS_ENDPOINT}/{user_id}", headers=headers)
        return parse_response(response)

    def get_user_attributes(self, user_id: UUID | str) -> dict:
        """Метод возвращает attributes пользователя user_id"""
        content = self.get_user_data(user_id=user_id)
        attributes = content.get('attributes')
        return attributes if attributes else {}

    def get_user_sessions(self, user_id: UUID | str):
        """Метод возвращает сессии пользователя"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("GET", f"{USERS_ENDPOINT}/{user_id}/sessions", headers=headers)
        return parse_response(response)

    def get_user_devices(self, user_access_token: str):
        """Метод возвращает устройства пользователя с которых он вошел в систему"""
        headers = {'Authorization': f'Bearer {user_access_token}', 'Content-Type': 'application/json'}
        response = requests.request("GET", f"{ACCOUNT_SESSION_URL}/devices", headers=headers)
        return parse_response(response)

    def set_user_attributes(self, user_id: UUID | str, attributes: dict):
        """Метод принимает на вход attributes и обновляет их у пользователя user_id"""
        payload = json.dumps({"attributes": attributes})
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("PUT", f"{USERS_ENDPOINT}/{user_id}", headers=headers, data=payload)
        return parse_response(response)

    def set_user_data(self, user_id: UUID | str, data: dict):
        """Метод принимает на вход основные данные пользователя и обновляет их у пользователя user_id"""
        payload = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("PUT", f"{USERS_ENDPOINT}/{user_id}", headers=headers, data=payload)
        return parse_response(response)

    def set_user_password(self, user_id: UUID | str, password: str, is_temp: bool = False):
        """Метод изменяет пароль пользователя user_id"""
        payload = json.dumps({"type": "password", "value": password, "temporary": is_temp})
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("PUT", f"{USERS_ENDPOINT}/{user_id}/reset-password", headers=headers, data=payload)
        return parse_response(response)

    def verify_user_email(self, user_id: UUID | str, params: dict = None):
        """Метод отправляет письмо на почту для подтверждения email"""
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request(
            "PUT",
            f"{USERS_ENDPOINT}/{user_id}/send-verify-email",
            params=params,
            headers=headers)
        return parse_response(response)

    def change_user_status(self, user_id: UUID | str, attributes: dict):
        """Метод блокирует/разблокирует пользователя"""
        payload = json.dumps(attributes)
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("PUT", f"{USERS_ENDPOINT}/{user_id}", headers=headers, data=payload)
        return parse_response(response)

    def delete_user_in_keycloak(self, user_id: UUID | str):
        """Метод удаляет пользователя user_id"""
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}
        response = requests.request(
            "DELETE",
            f"{USERS_ENDPOINT}/{user_id}",
            headers=headers)
        return parse_response(response)

    def delete_user_session(self, session_id: UUID | str):
        """Метод удаляет заданную сессию session_id"""
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json', }
        response = requests.request(
            "DELETE",
            f"{ADMIN_SESSION_URL}/{session_id}",
            headers=headers)
        return parse_response(response)

    def delete_user_sessions(self, sessions: list[UUID]):
        """Метод удаляет заданные сессии sessions"""
        for session in sessions:
            self.delete_user_session(session_id=session)
        return True

    def create_user_in_keycloak(self, username: str, first_name: str, last_name: str, middle_name: str, short_id: str):
        """Метод создает пользователя в KeyCloak"""
        now = int(timezone.now().timestamp())
        payload = json.dumps({
            "createdTimestamp": now,
            "username": username,
            "enabled": True,
            "totp": False,
            "emailVerified": False,
            "firstName": first_name,
            "lastName": last_name,
            "attributes": {
                "middleName": middle_name,
                "phoneNumber": username,
                "shortId": short_id
            }
        })
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}

        response = requests.request(
            "POST",
            USERS_ENDPOINT,
            headers=headers,
            data=payload)
        return parse_response(response)

    def check_username_existence(self, username: str) -> bool:
        """Метод проверяет, существует ли в Keycloak пользователь с переданным username."""

        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("GET", f'{USERS_ENDPOINT}?username={username}', headers=headers)
        try:
            content = parse_response(response)
            for user in content:
                if user['username'] == username:
                    return True
        except KeycloakResponseException:
            return False
        return False

    def check_email_existence(self, email: str) -> bool:
        """Метод проверяет, существует ли в Keycloak пользователь с переданным email"""

        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("GET", f'{USERS_ENDPOINT}?email={email}', headers=headers)

        try:
            content = parse_response(response)
            for user in content:
                if user['email'] == email:
                    return True
        except KeycloakResponseException:
            return False
        return False

    def execute_actions_via_email(self, user_id: UUID | str, actions: list):
        """Метод отправляет пользователю по почте запрос на совершение действие actions"""
        payload = json.dumps(actions)
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("PUT", f"{USERS_ENDPOINT}/{user_id}/execute-actions-email", headers=headers,
                                    data=payload)
        return parse_response(response)

    def logout_user(self, user_id: UUID | str):
        """Метод удаляет все сессии пользователя"""
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("POST", f"{ADMIN_URL}/users/{user_id}/logout", headers=headers)
        return parse_response(response)

    def impersonate_user(self, user_id: UUID | str):
        """Метод позволяет войти в систему от имени пользователя user_id"""
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.request("POST", f"{ADMIN_URL}/users/{user_id}/impersonation", headers=headers)
        parsed_response = parse_response(response)
        cookies = response.cookies.get_dict()

        return parsed_response, cookies
