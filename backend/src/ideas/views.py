import logging
import uuid

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action
from core.utils.exceptions import BadRequestException, S3ConnectionError, S3UploadError, S3DownloadError
from core.utils.files import S3Wrapper
from core.utils.http import Response, clean_get_params
from core.utils.notification import telegram_message
from ideas.models import Idea, IdeaComment, IdeaDocument, IdeaLike, IdeaCategory
from ideas.paginators import aux_ideas_paginator, aux_comments_paginator, aux_category_paginator
from ideas.serializers.serializers import IdeaSerializer, WriteIdeaSerializer, \
    IdeaSettingsSerializer, IdeaInformationSerializer, CommentSerializer, UploadFileSerializer, IdeaDocumentsSerializer, \
    IdeaLikeSerializer, IdeaCategorySerializer
from settings.settings import S3_IDEA_FILES_BUCKET

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaView(APIView):
    def __init__(self):
        super().__init__()
        self.show_statuses = None
        self.idea = None
        self.idea_id = None

    def dispatch(self, request, *args, **kwargs):
        self.idea_id = kwargs.get('idea_id')
        if self.idea_id:
            try:
                if request.method in ['PUT', 'DELETE']:
                    if kwargs.get('is_admin'):
                        self.idea = Idea.objects.get(id=self.idea_id)
                    else:
                        try:
                            self.idea = Idea.objects.get(id=self.idea_id, author=kwargs.get('user'))
                        except Idea.DoesNotExist:
                            return Response(status=403, content='Нет доступа')
                else:
                    if kwargs.get('is_admin'):
                        self.idea = Idea.objects.get(id=self.idea_id)
                    else:
                        self.idea = Idea.objects.get(
                            Q(id=self.idea_id) & (Q(settings__is_public=True) | Q(author=kwargs.get('user'))))
            except Idea.DoesNotExist:
                return Response({'message': 'Идея не найдена'}, status=404)
        self.show_statuses = [Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]
        if kwargs.get('is_admin'):
            self.show_statuses = [Idea.STATUS_APPROVED, Idea.STATUS_REJECTED, Idea.STATUS_CREATED,
                                  Idea.STATUS_ON_MODERATION, Idea.STATUS_NEED_WORK, Idea.STATUS_REJECTED,
                                  Idea.STATUS_FINISHED]
        sandbox = request.GET.get('sandbox')
        if sandbox and sandbox.lower() == 'true':
            self.show_statuses = [Idea.STATUS_ON_MODERATION]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.idea_id:
            return Response(IdeaSerializer(self.idea, context={"kwargs": kwargs}).data)
        else:
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            return aux_ideas_paginator(Idea.objects.filter(status__in=self.show_statuses, settings__is_public=True),
                                       *get_params, kwargs=kwargs)

    def post(self, request, *args, **kwargs):
        if self.idea_id:
            return Response(status=400, content='Неверный запрос')
        serializer = WriteIdeaSerializer(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=201, content={"id": str(instance.id)})

    def put(self, request, *args, **kwargs):
        if not self.idea_id:
            return Response(status=400, content='Неверный запрос, идентификатор идеи не указан')
        serializer = WriteIdeaSerializer(instance=self.idea, data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=204)

    def delete(self, request, *args, **kwargs):
        if not self.idea_id:
            return Response(status=400, content='Неверный запрос')
        self.idea.delete()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaSettingsView(APIView):

    def __init__(self):
        super().__init__()
        self.idea = None
        self.idea_id = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.idea_id = kwargs['idea_id']
            if kwargs.get('is_admin'):
                self.idea = Idea.objects.get(id=self.idea_id)
            else:
                self.idea = Idea.objects.get(id=self.idea_id, author=kwargs.get('user'))
        except (KeyError, Idea.DoesNotExist):
            return Response(status=400, content='Неверный запрос')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        settings = IdeaSettingsSerializer(self.idea.settings).data
        return Response(settings)

    def put(self, request, *args, **kwargs):
        serializer = IdeaSettingsSerializer(instance=self.idea.settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaStatusView(APIView):

    def __init__(self):
        super().__init__()
        self.user_is_admin = None
        self.idea = None
        self.idea_id = None

    def dispatch(self, request, *args, **kwargs):
        self.user_is_admin = kwargs.get('is_admin')
        if request.method == 'PUT':
            try:
                self.idea_id = kwargs['idea_id']
                if self.user_is_admin:
                    self.idea = Idea.objects.get(id=self.idea_id)
                else:
                    self.idea = Idea.objects.get(id=self.idea_id, author=kwargs.get('user'))
            except (KeyError, Idea.DoesNotExist):
                return Response(status=400, content='Неверный запрос')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        result = {"payload": []}
        for index, status in enumerate(Idea.STATUS_CHOICES):
            result["payload"].append({
                "id": index,
                'status': status[0],
                'name': status[1],
                'is_admin': True if status[0] in [Idea.STATUS_NEED_WORK, Idea.STATUS_REJECTED,
                                                  Idea.STATUS_APPROVED] else False,
            })
        return Response(result)

    def put(self, request, *args, **kwargs):
        if not self.idea:
            return Response(status=400, content='Неверный запрос, идентификатор идеи не указан')
        status = request.data.get('status')
        comment = request.data.get('comment')
        if self.user_is_admin:
            if status == Idea.STATUS_APPROVED:
                self.idea.approve(comment)
            elif status == Idea.STATUS_REJECTED:
                self.idea.reject(comment)
            elif status == Idea.STATUS_ON_MODERATION:
                self.idea.on_moderation(comment)
            elif status == Idea.STATUS_NEED_WORK:
                self.idea.need_work(comment)
            elif status == Idea.STATUS_FINISHED:
                self.idea.finished(comment)
            else:
                return Response(status=400, content='Неверный запрос. Нет такого статуса')
            return Response(status=204)
        else:
            if (self.idea.status == Idea.STATUS_CREATED or self.idea.status == Idea.STATUS_NEED_WORK) \
                    and status == Idea.STATUS_ON_MODERATION:
                self.idea.on_moderation(comment)
                return Response(status=204)
            elif status == Idea.STATUS_FINISHED:
                self.idea.finished(comment)
                return Response(status=204)
            else:
                return Response(status=400, content='Неверный запрос или недостаточно прав')


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaInformationView(APIView):

    def __init__(self):
        super().__init__()
        self.idea_id = None
        self.idea = None

    def dispatch(self, request, *args, **kwargs):
        self.idea_id = kwargs.get('idea_id')

        try:
            if kwargs.get('is_admin'):
                self.idea = Idea.objects.get(id=self.idea_id)
            else:
                self.idea = Idea.objects.get(id=self.idea_id, author=kwargs.get('user'))
        except Idea.DoesNotExist:
            return Response(status=400, content='Неверный запрос')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.idea:
            return Response(status=400, content='Неверный запрос')
        result = IdeaInformationSerializer(self.idea.information).data
        return Response(result)

    def put(self, request, *args, **kwargs):
        if not self.idea_id:
            return Response(status=400, content='Неверный запрос')
        serializer = IdeaInformationSerializer(instance=self.idea.information, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaCommentsView(APIView):

    def __init__(self):
        super().__init__()
        self.comment = None
        self.comment_id = None
        self.idea_id = None
        self.idea = None

    def dispatch(self, request, *args, **kwargs):
        self.idea_id = kwargs.get('idea_id')
        if self.idea_id:
            try:
                self.idea = Idea.objects.get(id=self.idea_id,
                                             status__in=[Idea.STATUS_APPROVED, Idea.STATUS_ON_MODERATION,
                                                         Idea.STATUS_FINISHED])
            except Idea.DoesNotExist:
                return Response({'message': 'Идея не найдена'}, status=404)
        self.comment_id = kwargs.get('comment_id')
        if self.comment_id:
            try:
                self.comment = IdeaComment.objects.get(id=self.comment_id, idea=self.idea)
            except IdeaComment.DoesNotExist:
                return Response({'message': 'Комментарий не найден'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.comment_id:
            return Response(CommentSerializer(self.comment).data)
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)
        return aux_comments_paginator(self.idea.comments.filter(parent=None), *get_params)

    def post(self, request, *args, **kwargs):
        if not self.idea_id:
            return Response(status=400, content='Неверный запрос')
        serializer = CommentSerializer(data=request.data, context={'kwargs': kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=201, content={"id": str(instance.id)})

    def delete(self, request, *args, **kwargs):
        if not self.idea_id and not kwargs.get('is_admin'):
            return Response(status=400, content='Неверный запрос')
        self.comment.text = "Данный комментарий был удален модератором"
        self.comment.save()
        return Response(status=204)


@method_decorator([tryexcept, auth], name='dispatch')
class IdeaFileUploadView(APIView):

    def __init__(self):
        super().__init__()
        self.idea = None
        self.idea_id = None
        self.s3 = None

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def dispatch(self, request, *args, **kwargs):
        self.idea_id = kwargs.get('idea_id')
        if self.idea_id:
            try:
                self.idea = Idea.objects.get(id=self.idea_id, author=kwargs.get('user'))
            except Idea.DoesNotExist:
                return Response({'message': 'Идея не найдена'}, status=404)
        try:
            self.s3 = S3Wrapper(bucket_name=S3_IDEA_FILES_BUCKET)
        except S3ConnectionError as error:
            logger.warning(error)
            telegram_message(f"Не удалось загрузить файл идеи на S3 у Пользователя: {self.user_id}")
            return Response(status=400, content="Не удалось загрузить идеи. Повторите попытку позже")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response(IdeaDocumentsSerializer(self.idea.documents.all(), many=True).data)

    def post(self, request, *args, **kwargs):
        url = request.GET.get('url')
        if url:
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException as error:
                logger.warning(error)
                return Response(status=400, content='Не удалось загрузить файл')
            if response.status_code != 200:
                return Response(status=400, content='Не удалось загрузить файл')
            file_name = url.split('/')[-1]
            file = ContentFile(response.content, name=file_name)
            file.seek(0)
            file_path = f'{uuid.uuid4()}_{file_name}'
            try:
                self.s3.upload_file(file_name, file.read())
                url = f"https://{S3_IDEA_FILES_BUCKET}.{self.s3.url.replace('https://', '')}/{file_path}"
            except S3ConnectionError as error:
                logger.warning(error)
                telegram_message(f"Не удалось загрузить файл идеи на S3 у Пользователя: {self.user_id}")
                return Response(status=400, content="Не удалось загрузить файл идеи. Повторите попытку позже")
        else:
            temp = request.FILES
            if 'file' not in temp:
                temp['file'] = request.FILES['image']
            data = UploadFileSerializer(data=temp)
            data.is_valid(raise_exception=True)
            file = data.save()
            file_name = file.file_name
            file_path = f"{uuid.uuid4()}_{file_name}"

            try:
                self.s3.upload_file(file_path, file.file)
                url = f"https://{S3_IDEA_FILES_BUCKET}.{self.s3.url.replace('https://', '')}/{file_path}"
            except (S3UploadError, S3DownloadError) as error:
                logger.warning(error)
                telegram_message(f"Не удалось загрузить файл идеи на S3 у Пользователя: {kwargs.get('user')}")
                return Response(status=400, content="Не удалось загрузить файл идеи. Повторите попытку позже")

        if request.GET.get('is_file', 'False').lower() == 'true':
            IdeaDocument.objects.create(idea=self.idea, path=file_path)
        return Response({
            "success": 1,
            "file": {
                "url": url
            }
        }, status=201)

    def delete(self, request, *args, **kwargs):
        url = request.GET.get('url')
        if url:
            try:
                self.s3.delete_file(url.split('/')[-1])
            except S3ConnectionError as error:
                logger.warning(error)
                telegram_message(f"Не удалось удалить файл идеи на S3 у Пользователя: {self.user_id}")
                return Response(status=400, content="Не удалось удалить файл идеи. Повторите попытку позже")
            return Response(status=204)
        else:
            if kwargs.get('file_id'):
                try:
                    file = IdeaDocument.objects.get(id=kwargs.get('file_id'), idea=self.idea)
                except IdeaDocument.DoesNotExist:
                    return Response({'message': 'Файл не найден'}, status=404)
                try:
                    self.s3.delete_file(file.path)
                except S3ConnectionError as error:
                    logger.warning(error)
                    telegram_message(f"Не удалось удалить файл идеи на S3 у Пользователя: {self.user_id}")
                    return Response(status=400, content="Не удалось удалить файл идеи. Повторите попытку позже")
                file.delete()
                return Response(status=204)
        return Response(status=400, content='Не удалось удалить файл')


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaLikesView(APIView):
    def __init__(self):
        super().__init__()
        self.idea = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.idea = Idea.objects.get(id=kwargs.get('idea_id'), settings__is_public=True,
                                         status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED,
                                                     Idea.STATUS_ON_MODERATION])
        except (Idea.DoesNotExist, ValueError):
            return Response({'message': 'Идея не найдена'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            like = IdeaLike.objects.get(idea=self.idea, author=kwargs.get('user'))
            like.delete()
        except (ObjectDoesNotExist, ValueError):
            pass
        serializer = IdeaLikeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(status=400, content="Не удалось поставить лайк")
        serializer.validated_data['idea'] = self.idea
        serializer.validated_data['author'] = kwargs.get('user')
        serializer.save()
        return Response(status=201)

    def get(self, request, *args, **kwargs):
        try:
            idea = Idea.objects.get(id=kwargs.get('idea_id'))
        except (Idea.DoesNotExist, ValueError):
            return Response({'message': 'Идея не найдена'}, status=404)
        return Response({'likes': idea.likes.count()}, status=200)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class IdeaCategoryView(APIView):
    def __init__(self):
        super().__init__()
        self.idea_id = None
        self.idea = None

    def dispatch(self, request, *args, **kwargs):
        # if not kwargs.get('is_admin'):
        #     return Response({'message': 'Нет доступа'}, status=403)
        self.idea_id = kwargs.get('idea_id')
        if self.idea_id:
            try:
                self.idea = Idea.objects.get(id=self.idea_id)
            except (Idea.DoesNotExist, ValueError):
                return Response({'message': 'Идея не найдена'}, status=404)
        if request.method in ['PUT', 'DELETE'] and not self.idea:
            return Response({'message': 'Идея не найдена'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.idea:
            # intellectual category recommendation
            tags = self.idea.tags.all()
            tags_count = {}
            for tag in tags:
                tags_count[tag] = Idea.objects.filter(tags__in=[tag]).count()
            tags_count = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:3]
            categories = []
            for tag, count in tags_count:
                categories += Idea.objects.filter(tags__in=[tag]).values_list('category', flat=True)
            categories_count = {}
            for category in categories:
                if category in categories_count:
                    categories_count[category] += 1
                else:
                    categories_count[category] = 1
            categories_count = sorted(categories_count.items(), key=lambda x: x[1], reverse=True)[:3]
            categories = []
            for category, count in categories_count:
                if category:
                    categories.append(IdeaCategory.objects.get(id=category))
            return Response({'payload': IdeaCategorySerializer(categories, many=True).data},
                            status=200)
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)
        return aux_category_paginator(IdeaCategory.objects.all(), *get_params)

    def put(self, request, *args, **kwargs):
        try:
            categories = IdeaCategory.objects.filter(id__in=request.data.get('categories'))
        except (IdeaCategory.DoesNotExist, ValueError):
            return Response({'message': 'Категории не найдены'}, status=404)
        self.idea.category.set(categories)
        return Response(status=204)

    def delete(self, request, *args, **kwargs):
        self.idea.category.clear()
        self.idea.save()
        return Response(status=204)
