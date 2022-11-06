import json
import logging
import random

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from chats.models import Chat, ChatNotification
from core.utils.decorators import tryexcept, log_action
from core.utils.exceptions import ChatCreationError, MessageSendError, PhotoUploadError, VKException, UserInfoError
from settings import settings
from settings.settings import VK_ACCESS_TOKEN, VK_GROUP_ID, VK_BOT_NAME

logger = logging.getLogger(__name__)


class VK:
    def __init__(self, access_token=VK_ACCESS_TOKEN, group_id=VK_GROUP_ID, v='5.103'):
        self.access_token = access_token
        self.group_id = group_id
        self.v = v

    @staticmethod
    def get_peer_id_from_chat_id(chat_id):
        return 2000000000 + chat_id

    @staticmethod
    def get_chat_id_from_peer_id(peer_id):
        return peer_id - 2000000000

    def pin_message(self, chat_id: int, conversation_message_id: int):
        url = "https://api.vk.com/method/messages.pin"
        peer_id = self.get_peer_id_from_chat_id(chat_id)
        payload = f'peer_id={peer_id}&conversation_message_id={conversation_message_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']
        except KeyError:
            raise MessageSendError("Не удалось закрепить сообщение")

    def set_activity(self, chat_id: int, type: str = "typing"):
        url = "https://api.vk.com/method/messages.setActivity"
        peer_id = self.get_peer_id_from_chat_id(chat_id)
        payload = f'peer_id={peer_id}&type={type}&group_id={self.group_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']
        except KeyError:
            raise VKException("Не удалось установить статус активности")

    def get_user_info(self, user_id: int | str):
        url = "https://api.vk.com/method/users.get"
        payload = f'user_ids={user_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            response = response.json()['response'][0]
            return response['first_name'], response['last_name']
        except UserInfoError:
            raise ("Не удалось получить информацию о человеке")

    def create_chat(self, title: str):
        url = "https://api.vk.com/method/messages.createChat"

        payload = f'title={title}&group_id={self.group_id}&users_id=55480954&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']
        except KeyError:
            raise ChatCreationError("Не удалось создать чат")

    def get_chat_link(self, chat_id: int):

        url = "https://api.vk.com/method/messages.getInviteLink"
        peer_id = self.get_peer_id_from_chat_id(chat_id)
        reset = 0
        payload = f'peer_id={peer_id}&reset={reset}&group_id={self.group_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']['link']
        except KeyError:
            raise ChatCreationError("Не удалось создать ссылку на чат")

    def send_message(self, chat_id: int, message: str):
        url = "https://api.vk.com/method/messages.send"
        peer_id = self.get_peer_id_from_chat_id(chat_id)
        random_id = random.randint(0, 1000000000)
        payload = f'peer_id={peer_id}&message={message}&random_id={random_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
        try:
            return response.json()['response']
        except KeyError:
            raise MessageSendError("Не удалось отправить сообщение")

    def get_chat_upload_server(self, chat_id: int):
        url = "https://api.vk.com/method/photos.getChatUploadServer"
        payload = f'chat_id={chat_id}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']['upload_url']
        except KeyError:
            raise PhotoUploadError("Не удалось получить ссылку для загрузки фото")

    def upload_chat_photo(self, upload_url: str, file):
        payload = f'access_token={self.access_token}&v={self.v}'
        files = [
            ('file',
             ('chat.webp', file, 'image/webp'))
        ]
        response = requests.request("POST", upload_url, params=payload.encode('utf-8'),
                                    files=files)

        try:
            return response.json()['response']
        except KeyError:
            raise PhotoUploadError("Не удалось загрузить фото")

    def set_chat_photo(self, chat_id: int, file: str):
        url = "https://api.vk.com/method/messages.setChatPhoto"
        payload = f'file={file}&access_token={self.access_token}&v={self.v}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

        try:
            return response.json()['response']
        except KeyError:
            raise PhotoUploadError("Не удалось загрузить фото")


@method_decorator([tryexcept, log_action], name='dispatch')
class VKCallbackView(APIView):
    vk = None
    group_id = None
    chat = None

    def dispatch(self, request, *args, **kwargs):
        self.vk = VK()
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            logger.error('Не удалось распарсить json')
            return HttpResponse("ok")
        if not self.check_security(body):
            logger.error('VK Callback security check failed')
            return HttpResponse('ok')
        return super().dispatch(request, *args, **kwargs)

    def check_security(self, body):
        secret = body.get('secret')
        group_id = body.get('group_id')
        if not secret or not group_id:
            return False
        if secret != settings.VK_SECRET_KEY or group_id != settings.VK_GROUP_ID:
            return False
        self.group_id = group_id
        return True

    def process_message_action_type(self, message_action_type: str, peer_id: int, from_id: int):

        if message_action_type == 'chat_invite_user':
            # Пользователь приглашен в чат
            pass
        elif message_action_type == 'chat_photo_update':
            # Обновилась фотография чата
            pass
        elif message_action_type == 'chat_photo_remove':
            # Удалилась фотография чата
            pass
        elif message_action_type == 'chat_title_update':
            # Обновилось название чата
            pass
        elif message_action_type == 'chat_create':
            # Создан чат
            pass
        elif message_action_type == 'chat_invite_user_by_link':
            # Пользователь присоединился к беседе по ссылке
            if self.chat.chat_type == Chat.TEAM_CHAT:
                user_first_name, user_last_name = self.vk.get_user_info(user_id=from_id)
                if self.chat.users_count == 0:
                    self.chat.users_count = 1
                    self.chat.save()
                    num = len(self.chat.name) % 8
                    file = open(f'core/logo/chat_{num}.webp', 'rb')
                    upload_url = self.vk.get_chat_upload_server(chat_id=self.chat.chat_id)
                    content = self.vk.upload_chat_photo(upload_url=upload_url, file=file)
                    self.vk.set_chat_photo(chat_id=self.chat.chat_id, file=content)
                    message = self.chat.get_team_chat_init_greeting_message(user_first_name=user_first_name)
                    self.vk.send_message(self.chat.chat_id, message)
                else:
                    message = self.chat.get_new_person_joined(user_first_name=user_first_name)
                    self.vk.send_message(self.chat.chat_id, message)
                    self.chat.users_count += 1
                    self.chat.save()
            if self.chat.chat_type == Chat.INTEREST_CHAT:
                if self.chat.users_count == 0:
                    self.chat.users_count = 1
                    self.chat.save()
                    num = len(self.chat.name) % 8
                    file = open(f'core/logo/chat_{num}.webp', 'rb')
                    upload_url = self.vk.get_chat_upload_server(chat_id=self.chat.chat_id)
                    content = self.vk.upload_chat_photo(upload_url=upload_url, file=file)
                    self.vk.set_chat_photo(chat_id=self.chat.chat_id, file=content)
                else:
                    self.chat.users_count += 1
                    self.chat.save()
        elif message_action_type == 'chat_kick_user':
            # Пользователь исключен из чата
            if self.chat.chat_type == Chat.TEAM_CHAT:
                message = self.chat.get_kicked_user_message()
                self.vk.send_message(self.chat.chat_id, message)
        elif message_action_type == 'chat_pin_message':
            # Сообщение закреплено
            pass
        elif message_action_type == 'chat_unpin_message':
            # Сообщение откреплено
            pass
        return None

    def process_message(self, text, peer_id):
        if VK_BOT_NAME in text:
            is_question = False
            if "?" in text:
                is_question = True
            chat_id = VK.get_chat_id_from_peer_id(peer_id=peer_id)
            self.vk.set_activity(chat_id=chat_id)
            message = self.chat.get_tag_message(is_question=is_question)
            self.vk.send_message(chat_id, message)
            ChatNotification.objects.create(chat=self.chat, message=text)

    def post(self, request, *args, **kwargs):
        """Парсинг запросов в чатах"""
        body = request.data
        action_type = body.get('type')
        if action_type == 'message_new':
            # Новое сообщение
            peer_id = body['object']['message']['peer_id']
            try:
                self.chat = Chat.objects.get(peer_id=peer_id)
            except ObjectDoesNotExist:
                return HttpResponse("ok")

            text = body['object']['message']['text']
            action = body['object']['message'].get('action')
            from_id = body['object']['message']['from_id']
            if action:
                message_action_type = action['type']
                self.process_message_action_type(message_action_type, peer_id, from_id)
            else:
                self.process_message(text, peer_id)

        return HttpResponse("ok")
