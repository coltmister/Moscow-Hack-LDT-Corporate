from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from chats.models import ChatNotification, Chat
from chats.paginator import chat_notification_paginator, chat_paginator
from chats.serializers import ChatSerializer
from core.utils.decorators import tryexcept, auth, admin_only, log_action
from core.utils.exceptions import BadRequestException, ChatCreationError
from core.utils.http import Response, clean_get_params
from core.vk_integration import VK
from teams.models import Team
from users.models import Interest


# Create your views here.
@method_decorator([tryexcept, auth, admin_only, log_action], name='dispatch')
class ChatNotificationsView(APIView):
    def get(self, request, chat_pk=None, *args, **kwargs):

        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)

        if chat_pk is not None:
            try:
                chat_notifications = ChatNotification.objects.filter(chat=chat_pk)
            except ChatNotification.DoesNotExist:
                return Response(status=404, content="Уведомление не найдено")
        else:
            chat_notifications = ChatNotification.objects.filter(is_read=False)

        return Response(chat_notification_paginator(chat_notifications, *get_params))

    def put(self, request, notification_pk, *args, **kwargs):
        try:
            notification = ChatNotification.objects.get(pk=notification_pk)
        except ChatNotification.DoesNotExist:
            return Response(status=404, content="Уведомление не найдено")
        notification.is_read = True
        notification.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class ChatsView(APIView):
    def get(self, request, chat_pk=None, *args, **kwargs):
        current_user = kwargs.get('user')
        if not chat_pk:
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            if current_user.is_admin:
                chats = Chat.objects.all()
            else:
                chats = Chat.objects.filter(chat_type=Chat.INTEREST_CHAT)
            return Response(chat_paginator(chats, *get_params))

        try:
            chat = Chat.objects.get(pk=chat_pk)
        except Chat.DoesNotExist:
            return Response(status=404, content="Чат не найден")

        if not current_user.is_admin and chat.chat_type == Chat.TEAM_CHAT:
            return Response(status=400, content="Вы не можете просматривать этот чат")

        return Response(ChatSerializer(chat).data)


#  Получить все чаты


@method_decorator([tryexcept, auth, admin_only, log_action], name='dispatch')
class CreateInterestChat(APIView):
    def post(self, request, interest_pk, *args, **kwargs):
        """Создать чат по интересу"""
        try:
            interest = Interest.objects.get(pk=interest_pk)
        except Interest.DoesNotExist:
            return Response(status=404, content="Интерес не найден")

        if interest.chat is not None:
            return Response(status=200, content=ChatSerializer(interest.chat).data)

        chat_name = request.data.get('name')
        if Chat.objects.filter(name=chat_name).exists():
            return Response(status=400, content="Чат с таким названием уже существует")
        vk = VK()
        try:
            vk_chat_id = vk.create_chat(chat_name)
            vk_chat_link = vk.get_chat_link(chat_id=vk_chat_id)
            num = len(chat_name) % 8
            file = open(f'core/logo/chat_{num}.webp', 'rb')
            upload_url = vk.get_chat_upload_server(chat_id=vk_chat_id)
            vk.upload_chat_photo(upload_url=upload_url, file=file)
        except ChatCreationError as error:
            return Response(status=400, content=error.message)

        chat = Chat.objects.create(chat_id=vk_chat_id, chat_link=vk_chat_link, name=chat_name,
                                   peer_id=VK.get_peer_id_from_chat_id(vk_chat_id))
        interest.chat = chat
        interest.save()

        return Response(status=201, content=ChatSerializer(chat).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class VKChatInviteLinkView(APIView):
    def get(self, request, team_pk, *args, **kwargs):
        user = kwargs.get('user')
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if not (team.team_leader == user or user in team.members.all()):
            return Response(status=400,
                            content="Вы не можете просматривать ссылку на чат данной команды, так как не являетесь ее лидером или участником")

        if team.chat is not None:
            return Response(status=201, content=ChatSerializer(team.chat).data)

        vk = VK()
        try:
            vk_chat_id = vk.create_chat(team.name)
            vk_chat_link = vk.get_chat_link(chat_id=vk_chat_id)
            num = len(team.name) % 8
            file = open(f'core/logo/chat_{num}.webp', 'rb')
            upload_url = vk.get_chat_upload_server(chat_id=vk_chat_id)
            vk.upload_chat_photo(upload_url=upload_url, file=file)
        except ChatCreationError as error:
            return Response(status=400, content=error.message)

        chat = Chat.objects.create(chat_id=vk_chat_id, chat_link=vk_chat_link, name=team.name,
                                   peer_id=VK.get_peer_id_from_chat_id(vk_chat_id))
        team.chat = chat
        team.save()
        return Response(status=201, content=ChatSerializer(chat).data)


@shared_task
def create_vk_team_chat(team_pk):
    """Создание чата в ВК"""
    try:
        team = Team.objects.get(id=team_pk)
    except ObjectDoesNotExist:
        return False, 'Команда не найдена'

    vk = VK()
    try:
        vk_chat_id = vk.create_chat(team.name)
        vk_chat_link = vk.get_chat_link(chat_id=vk_chat_id)
        num = len(team.name) % 8
        file = open(f'core/logo/chat_{num}.webp', 'rb')
        upload_url = vk.get_chat_upload_server(chat_id=vk_chat_id)
        vk.upload_chat_photo(upload_url=upload_url, file=file)
    except ChatCreationError as error:
        return False, error.message

    chat = Chat.objects.create(chat_id=vk_chat_id, chat_link=vk_chat_link, name=team.name,
                               peer_id=VK.get_peer_id_from_chat_id(vk_chat_id))
    team.chat = chat
    team.save()
    return True, 'Чат успешно создан'


@shared_task
def create_interest_chat(interest_pk):
    """Создание чата по интересам"""
    try:
        interest = Interest.objects.get(id=interest_pk)
    except Interest.DoesNotExist:
        return False, 'Интерес не найден'

    chat_name = interest.name
    vk = VK()
    try:
        vk_chat_id = vk.create_chat(chat_name)
        vk_chat_link = vk.get_chat_link(chat_id=vk_chat_id)
        num = len(chat_name) % 8
        file = open(f'core/logo/chat_{num}.webp', 'rb')
        upload_url = vk.get_chat_upload_server(chat_id=vk_chat_id)
        vk.upload_chat_photo(upload_url=upload_url, file=file)
    except ChatCreationError as error:
        return False, error.message

    chat = Chat.objects.create(chat_id=vk_chat_id, chat_link=vk_chat_link, name=chat_name,
                               peer_id=VK.get_peer_id_from_chat_id(vk_chat_id))
    interest.chat = chat
    interest.save()
    return True, 'Чат успешно создан'