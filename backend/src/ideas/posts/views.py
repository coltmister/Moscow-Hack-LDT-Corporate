import logging
import uuid

import requests
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action
from core.utils.exceptions import BadRequestException, S3ConnectionError, S3UploadError, S3DownloadError
from core.utils.files import S3Wrapper
from core.utils.http import Response, clean_get_params
from core.utils.notification import telegram_message
from ideas.models import Post, PostLike, PostComment, PostDocument
from ideas.paginators import aux_comments_paginator
from ideas.posts.paginators import aux_posts_paginator
from ideas.posts.serializers import PostSerializer, WritePostSerializer, PostLikeSerializer, PostCommentSerializer, \
    PostDocumentsSerializer
from ideas.serializers.serializers import UploadFileSerializer
from settings.settings import S3_POST_FILES_BUCKET

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class PostView(APIView):
    def __init__(self):
        super().__init__()
        self.idea_id = None
        self.post_obj = None
        self.post_id = None

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs.get('post_id')
        self.idea_id = kwargs.get('idea_id')
        if self.post_id:
            try:
                if request.method in ['PUT', 'DELETE']:

                    if kwargs.get('is_admin'):
                        self.post_obj = Post.objects.get(id=self.post_id, idea__id=self.idea_id)
                    else:
                        try:
                            self.post_obj = Post.objects.get(id=self.post_id, author=kwargs.get('user'),
                                                             idea__id=self.idea_id, idea__author=kwargs.get('user'))
                        except Post.DoesNotExist:
                            return Response(status=403, content='Нет доступа')
                else:
                    self.post_obj = Post.objects.get(id=self.post_id, idea__id=self.idea_id)
            except Post.DoesNotExist:
                return Response({'message': 'Пост не найден'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.post_id:
            return Response(PostSerializer(self.post_obj, context={"kwargs": kwargs}).data)
        elif self.idea_id:
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            return aux_posts_paginator(Post.objects.filter(idea__id=self.idea_id), *get_params)
        else:
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            return aux_posts_paginator(Post.objects.all(), *get_params)

    def post(self, request, *args, **kwargs):
        if self.post_id:
            return Response(status=400, content='Неверный запрос')
        serializer = WritePostSerializer(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=201, content={"id": str(instance.id)})

    def put(self, request, *args, **kwargs):
        if not self.post_id:
            return Response(status=400, content='Неверный запрос, идентификатор идеи не указан')
        serializer = WritePostSerializer(instance=self.post_obj, data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=204)

    def delete(self, request, *args, **kwargs):
        if not self.post_id:
            return Response(status=400, content='Неверный запрос')
        self.post_obj.delete()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class PostLikesView(APIView):
    def __init__(self):
        super().__init__()
        self.post_obj = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.post_obj = Post.objects.get(id=kwargs.get('post_id'))
        except Post.DoesNotExist:
            return Response({'message': 'Идея не найдена'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            like = PostLike.objects.get(post=self.post_obj, author=kwargs.get('user'))
            like.delete()
            return Response(status=204)
        except PostLike.DoesNotExist:
            serializer = PostLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['post'] = self.post_obj
            serializer.validated_data['author'] = kwargs.get('user')
            serializer.save()
            return Response(status=201)

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('post_id'))
        except Post.DoesNotExist:
            return Response({'message': 'Идея не найдена'}, status=404)
        return Response({'likes': post.likes.count()}, status=200)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class PostCommentsView(APIView):

    def __init__(self):
        super().__init__()
        self.comment = None
        self.comment_id = None
        self.post_id = None
        self.post_obj = None

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs.get('post_id')
        if self.post_id:
            try:
                self.post_obj = Post.objects.get(id=self.post_id)
            except Post.DoesNotExist:
                return Response({'message': 'Пост не найдена'}, status=404)
        self.comment_id = kwargs.get('comment_id')
        if self.comment_id:
            try:
                self.comment = PostComment.objects.get(id=self.comment_id, post=self.post_obj)
            except PostComment.DoesNotExist:
                return Response({'message': 'Комментарий не найден'}, status=404)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.comment_id:
            return Response(PostCommentSerializer(self.comment).data)
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)
        return aux_comments_paginator(self.post_obj.comments.filter(parent=None), *get_params, post=True)

    def post(self, request, *args, **kwargs):
        if not self.post_id:
            return Response(status=400, content='Неверный запрос')
        serializer = PostCommentSerializer(data=request.data, context={'kwargs': kwargs})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=201, content={"id": str(instance.id)})

    def delete(self, request, *args, **kwargs):
        if not self.post_id and not kwargs.get('is_admin'):
            return Response(status=400, content='Неверный запрос')
        self.comment.text = "Данный комментарий был удален модератором"
        self.comment.save()
        return Response(status=204)


@method_decorator([tryexcept, auth], name='dispatch')
class PostFileUploadView(APIView):

    def __init__(self):
        super().__init__()
        self.post_obj = None
        self.post_id = None
        self.s3 = None

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs.get('post_id')
        if self.post_id:
            try:
                self.post_obj = Post.objects.get(id=self.post_id, author=kwargs.get('user'))
            except Post.DoesNotExist:
                return Response({'message': 'Идея не найдена'}, status=404)
        else:
            return Response(status=400, content='Неверный запрос')
        try:
            self.s3 = S3Wrapper(bucket_name=S3_POST_FILES_BUCKET)
        except S3ConnectionError as error:
            logger.warning(error)
            telegram_message(f"Не удалось загрузить файл идеи на S3 у Пользователя: {self.user_id}")
            return Response(status=400, content="Не удалось загрузить идеи. Повторите попытку позже")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response(PostDocumentsSerializer(self.post_obj.documents.all(), many=True).data)

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
                url = f"https://{S3_POST_FILES_BUCKET}.{self.s3.url.replace('https://', '')}/{file_path}"
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
                url = f"https://{S3_POST_FILES_BUCKET}.{self.s3.url.replace('https://', '')}/{file_path}"
            except (S3UploadError, S3DownloadError) as error:
                logger.warning(error)
                telegram_message(f"Не удалось загрузить файл идеи на S3 у Пользователя: {kwargs.get('user')}")
                return Response(status=400, content="Не удалось загрузить файл идеи. Повторите попытку позже")

        if request.GET.get('is_file', 'False').lower() == 'true':
            PostDocument.objects.create(post=self.post_obj, path=file_path)
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
                    file = PostDocument.objects.get(id=kwargs.get('file_id'), post=self.post_obj)
                except PostDocument.DoesNotExist:
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
