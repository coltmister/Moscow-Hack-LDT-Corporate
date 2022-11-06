import io
import logging
import uuid

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action, admin_only
from core.utils.exceptions import BadRequestException, S3UploadError, S3DeleteError, S3ConnectionError, S3DownloadError, \
    TokenObtainException, KeycloakResponseException
from core.utils.files import S3Wrapper
from core.utils.http import Response, clean_get_params
from core.utils.notification import telegram_message
from iam.keycloak import Keycloak
from ideas.models import Idea
from ideas.serializers.serializers import UploadFileSerializer, IdeaSerializer
from settings.settings import S3_USER_PHOTO_BUCKET
from teams.serializers import TeamSerializer
from users.models import User
from users.paginator import user_paginator
from users.serializers import UserSerializer, UserProfileSerializer, UserProfileSettingsSerializer, \
    UserAddInfoSerializer, WriteUserAddInfoSerializer

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserIdeasView(APIView):

    def get(self, request, user_pk=None, *args, **kwargs):
        """Возвращает список идей пользователя."""
        user = kwargs.get('user')
        if user_pk:
            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content=f"Пользователь не найден")
        ideas = Idea.objects.filter(Q(author=user) | Q(team__members__in=[user]))

        return Response(IdeaSerializer(ideas, many=True, context={"kwargs": kwargs}).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserMeView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Метод возвращает информацию о пользователе
        """
        user = kwargs.get('user')
        return Response(UserSerializer(user).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserView(APIView):
    """Просмотр пользователей/заданного пользователя"""

    def get(self, request, user_pk=None, username_pk=None, *args, **kwargs):
        """Просмотр всех пользователей или заданного пользователя"""

        if not user_pk and not username_pk:
            users = User.objects.all()
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            return Response(user_paginator(users, *get_params))

        if user_pk:
            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")
        else:
            try:
                user = User.objects.get(username=username_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")

        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserProfileView(APIView):
    """CRUD профиля пользователя"""
    user = None

    def dispatch(self, request, *args, **kwargs):
        kwargs["me"] = False
        if request.path.endswith('/me/profile'):
            kwargs["me"] = True
        self.user = kwargs.get('user')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_pk=None, me=None, *args, **kwargs):
        if me:
            user = self.user
        else:
            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")

        serializer = UserProfileSerializer(instance=user.profile, context={'me': me})
        return Response(serializer.data)

    def put(self, request, user_pk=None, me=None, *args, **kwargs):
        if me:
            user = self.user
        else:
            if not self.user.is_admin:
                return Response(status=403, content="Обновлять профиль другого пользователя может только администратор")

            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")

        serializer = UserProfileSerializer(instance=user.profile, data=request.data, context={'me': me, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(status=400, content=serializer.errors)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserProfileSettingsView(APIView):
    """Получить/задать настройки своего профиля"""

    def get(self, request, *args, **kwargs):
        user = kwargs.get('user')
        serializer = UserProfileSettingsSerializer(instance=user.profile.profile_settings)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = kwargs.get('user')
        serializer = UserProfileSettingsSerializer(instance=user.profile.profile_settings, data=request.data)
        if not serializer.is_valid():
            return Response(status=400, content=serializer.errors)

        serializer.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserAddInfoView(APIView):
    """Добавление информации о пользователе"""
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_pk=None, *args, **kwargs):
        if user_pk:
            user_me = False
            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")
        else:
            user = self.user
            user_me = True
        serializer = UserAddInfoSerializer(instance=user.add_info, context={'me': user_me})
        return Response(serializer.data)

    def put(self, request, user_pk=None, *args, **kwargs):
        if user_pk:
            if not self.user.is_admin:
                return Response(status=400,
                                content="Обновлять доп. информацию о пользователе может только администратор")
            # Админ может изменять доп. информацию о любом пользователе
            try:
                user = User.objects.get(id=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")
        else:
            user = kwargs.get('user')
        serializer = WriteUserAddInfoSerializer(data=request.data, instance=user.add_info)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserAvatarView(APIView):
    user = None
    s3 = None
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')

        try:
            self.s3 = S3Wrapper(bucket_name=S3_USER_PHOTO_BUCKET)
        except S3ConnectionError as error:
            logger.warning(error)
            telegram_message(f"Не удалось загрузить файл проекта на S3 у Пользователя: {self.user.id}")
            return Response(status=400, content="Ошибка при соединении с сервером S3. Повторите попытку позже")

        return super().dispatch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        data = UploadFileSerializer(data=request.FILES)
        data.is_valid(raise_exception=True)
        file = data.save()
        file = file.file
        avatar_path = f"{self.user.id}_{str(uuid.uuid4())}.jpg"
        thumbnail_path = f"{self.user.id}_{str(uuid.uuid4())}.jpg"

        # Привожу фото к JPEG формату, чтобы не волноваться про остальные виды
        try:
            if isinstance(file, io.BytesIO):
                photo = Image.open(file)
            else:
                photo = Image.open(io.BytesIO(file))
        except Exception as error:
            logger.warning(error)
            return Response(status=400, content="Ошибка в файле фотографии")
        if photo.mode in ("RGBA", "P"):
            photo = photo.convert('RGB')
        photo_data = io.BytesIO()
        photo.save(photo_data, 'JPEG', quality=100)
        # Создаю миниатюру для фото человека
        thumbnail = Image.open(photo_data)
        max_size = (300, 400)
        thumbnail.thumbnail(max_size)
        if thumbnail.mode in ("RGBA", "P"):
            thumbnail = thumbnail.convert('RGB')
        thumbnail_data = io.BytesIO()
        thumbnail.save(thumbnail_data, 'JPEG', quality=100)
        # Нужно перекинуть байты в начало, иначе ничего не сохранится
        thumbnail_data.seek(0)
        photo_data.seek(0)

        try:
            self.s3.upload_file(avatar_path, photo_data)
            avatar_url = f"https://{S3_USER_PHOTO_BUCKET}.{self.s3.url.replace('https://', '')}/{avatar_path}"
        except (S3UploadError, S3DownloadError) as error:
            logger.warning(error)
            telegram_message(f"Не удалось загрузить фотографию на S3 у Пользователя: {self.user.id}")
            return Response(status=400, content="Не удалось загрузить фотографию. Повторите попытку позже")

        try:
            self.s3.upload_file(thumbnail_path, thumbnail_data)
            thumbnail_url = f"https://{S3_USER_PHOTO_BUCKET}.{self.s3.url.replace('https://', '')}/{thumbnail_path}"
        except (S3UploadError, S3DownloadError) as error:
            logger.warning(error)
            telegram_message(f"Не удалось загрузить фотографию на S3 у Пользователя: {self.user.id}")
            return Response(status=400, content="Не удалось загрузить фотографию. Повторите попытку позже")

        self.user.profile.avatar = avatar_url
        self.user.profile.avatar_thumbnail = thumbnail_url
        self.user.profile.save()
        return Response(status=204)

    def delete(self, request, *args, **kwargs):

        try:
            self.s3.delete_file(self.user.profile.avatar)
        except S3DeleteError as error:
            logger.warning(error)
            telegram_message(f"Не удалось удалить фото на S3 у Пользователя: {self.user.id}")
        try:
            self.s3.delete_file(self.user.profile.avatar_thumbnail)
        except S3DeleteError as error:
            logger.warning(error)
            telegram_message(f"Не удалось удалить миниатюру на S3 у Пользователя: {self.user.id}")

        # Обновляю информацию в пользователе
        self.user.profile.avatar = None
        self.user.profile.avatar_thumbnail = None
        self.user.profile.save()

        return Response(status=204)


@method_decorator([tryexcept, auth, admin_only, log_action], name='dispatch')
class VerifyUser(APIView):
    def put(self, request, user_pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Пользователь не найден")

        is_verified = True if request.data.get('is_verified', False) else False
        user.is_verified = is_verified
        user.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, admin_only, log_action], name='dispatch')
class PromoteUserToAdmin(APIView):
    def put(self, request, user_pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Пользователь не найден")

        try:
            keycloak = Keycloak()
        except TokenObtainException as error:
            return Response(status=400, content=error.message)

        is_admin = True if request.data.get('is_admin', False) else False
        try:
            keycloak.set_user_attributes(user.id, {'is_admin': is_admin,
                                                   'dob': str(user.profile.birthdate),
                                                   'patronymic': user.patronymic
                                                   })
        except KeycloakResponseException:
            return Response(status=400, content="Не удалось присвоить пользователю роль администратора")
        user.is_admin = is_admin
        user.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserTeamsListView(APIView):
    """Команды, в которых состоит заданный пользователь"""

    def get(self, request, user_pk=None, *args, **kwargs):
        current_user = kwargs.get('user')
        is_team_lead = request.query_params.get('is_team_leader', 'false')
        is_team_lead = True if is_team_lead.lower() == 'true' else False
        if user_pk:
            try:
                user = User.objects.get(pk=user_pk)
            except ObjectDoesNotExist:
                return Response(status=404, content="Пользователь не найден")
        else:
            user = kwargs.get('user')

        teams = user.teams.all()
        if is_team_lead:
            teams = teams.filter(team_leader=user)
        serializer = TeamSerializer(teams, many=True, context={'current_user': current_user})
        return Response(serializer.data, status=200)
