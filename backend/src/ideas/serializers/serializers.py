import uuid
from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import teams
from ideas.models import Idea, IdeaCategory, IdeaSettings, IdeaInformation, IdeaComment, IdeaDocument, IdeaLike, Post
from settings.settings import S3_IDEA_FILES_BUCKET, S3_SERVER
from teams.models import Team
from users.models import User, Interest
from users.serializers import UserSerializer


class IdeaCategorySerializer(serializers.ModelSerializer):
    idea_count = serializers.SerializerMethodField()

    def get_idea_count(self, obj):
        ideas_count = obj.ideas.count()
        obj.ideas_count = ideas_count
        obj.save()
        return ideas_count

    class Meta:
        model = IdeaCategory
        fields = ['id', 'name', 'description', 'idea_count']


class IdeaInterestSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose')
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        return str(obj.parent.id) if obj.parent else None

    class Meta:
        model = Interest
        fields = ['id', 'name', 'parent']


class IdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    status = serializers.SerializerMethodField()
    category = IdeaCategorySerializer(many=True)
    tags = IdeaInterestSerializer(many=True)
    subscribers_count = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()
    settings = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    information = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    last_post = serializers.SerializerMethodField()
    my_reaction = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_status(self, obj):
        return {
            "id": [x[0] for x in Idea.STATUS_CHOICES].index(obj.status),
            "name": obj.get_status_display()
        }

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_subscribers(self, obj):
        return UserSerializer(obj.subscribers.all()[:3], many=True).data

    def get_settings(self, obj):
        return IdeaSettingsSerializer(obj.settings).data

    def get_can_edit(self, obj):
        return (obj.author == self.context['kwargs'].get('user')) or self.context['kwargs'].get('is_admin')

    def get_information(self, obj):
        return IdeaInformationSerializer(obj.information).data

    def get_reactions(self, obj):
        likes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.LIKE).distinct()
        dislikes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.DISLIKE).distinct()
        super_likes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.SUPER_LIKE).distinct()
        neutrals = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.NEUTRAL).distinct()
        super_dislikes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.SUPER_DISLIKE).distinct()
        return {
            "likes": {
                "users": UserSerializer(instance=likes[:3], many=True).data,
                "count": likes.count()
            },
            "super_likes": {
                "users": UserSerializer(instance=super_likes[:3], many=True).data,
                "count": super_likes.count()
            },
            "dislikes": {
                "users": UserSerializer(instance=dislikes[:3], many=True).data,
                "count": dislikes.count()
            },
            "neutrals": {
                "users": UserSerializer(instance=neutrals[:3], many=True).data,
                "count": neutrals.count()
            },
            "super_dislikes": {
                "users": UserSerializer(instance=super_dislikes[:3], many=True).data,
                "count": super_dislikes.count()
            },

        }

    def get_last_post(self, obj):
        return BriefPostSerializer(obj.get_last_post()).data

    def get_my_reaction(self, obj):
        user = self.context['kwargs'].get('user')
        if user:
            try:
                like = IdeaLike.objects.get(idea=obj, author=user)
                return IdeaLikeSerializer(like).data
            except IdeaLike.DoesNotExist:
                return None
        return None

    def get_team(self, obj):
        team_obj = Team.objects.filter(idea=obj).first()
        if team_obj:
            return teams.serializers.TeamSerializer(team_obj,
                                                    context={"current_user": self.context['kwargs'].get('user')}).data
        return None

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'idea_json',
                  'author', 'status', 'category', 'tags', 'links', 'rating', 'created_at', 'updated_at', 'subscribers',
                  'subscribers_count', 'can_edit', 'settings', 'information', 'reactions', 'last_post',
                  'my_reaction', 'team']


class BriefIdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    status = serializers.SerializerMethodField()
    category = IdeaCategorySerializer(many=True)
    tags = IdeaInterestSerializer(many=True)
    subscribers_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    reactions_count = serializers.SerializerMethodField()
    my_reaction = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    def get_status(self, obj):
        return {
            "id": [x[0] for x in Idea.STATUS_CHOICES].index(obj.status),
            "name": obj.get_status_display()
        }

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_subscribers(self, obj):
        return UserSerializer(obj.subscribers.all(), many=True).data

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.filter(value=IdeaLike.LIKE).count() + (obj.likes.filter(value=IdeaLike.SUPER_LIKE).count() * 2)

    def get_reactions_count(self, obj):
        return obj.likes.count()

    def get_my_reaction(self, obj):
        kwargs = self.context.get('kwargs')
        user = None
        if kwargs:
            user = self.context.get('kwargs').get('user')
        if user:
            try:
                like = IdeaLike.objects.get(idea=obj, author=user)
                return IdeaLikeSerializer(like).data
            except (ValueError, IdeaLike.DoesNotExist):
                return None
        return None

    def get_reactions(self, obj):
        likes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.LIKE).distinct()
        dislikes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.DISLIKE).distinct()
        super_likes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.SUPER_LIKE).distinct()
        neutrals = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.NEUTRAL).distinct()
        super_dislikes = User.objects.filter(likes__idea=obj, likes__value=IdeaLike.SUPER_DISLIKE).distinct()
        return {
            "likes": {
                "users": UserSerializer(instance=likes[:3], many=True).data,
                "count": likes.count()
            },
            "super_likes": {
                "users": UserSerializer(instance=super_likes[:3], many=True).data,
                "count": super_likes.count()
            },
            "dislikes": {
                "users": UserSerializer(instance=dislikes[:3], many=True).data,
                "count": dislikes.count()
            },
            "neutrals": {
                "users": UserSerializer(instance=neutrals[:3], many=True).data,
                "count": neutrals.count()
            },
            "super_dislikes": {
                "users": UserSerializer(instance=super_dislikes[:3], many=True).data,
                "count": super_dislikes.count()
            },

        }

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'idea_json',
                  'author', 'status', 'category', 'tags',
                  'rating', 'created_at', 'updated_at',
                  'subscribers_count', 'comments_count',
                  'likes_count', 'reactions_count', 'my_reaction', 'reactions']


class BriefPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    idea = BriefIdeaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'idea', 'description', 'post_json', 'author', 'rating')


class WriteIdeaSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Interest.objects.all())

    def create(self, validated_data):
        """
        Create tags, update, delete and set
        """
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            validated_data['author'] = self.context['kwargs'].get('user')
            idea = Idea.objects.create(**validated_data)
            idea.tags.set([tag for tag in tags])
            idea.save()
        else:
            validated_data['author'] = self.context['kwargs'].get('user')
            idea = Idea.objects.create(**validated_data)
        return idea

    def update(self, instance, validated_data):
        """
        Update tags, update, delete and set
        """
        instance = super().update(instance, validated_data)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set([tag for tag in tags])
        return instance

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'idea_json', 'tags', 'links']


class IdeaSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaSettings
        fields = ['id', 'is_public', 'is_commentable']


class IdeaInformationSerializer(serializers.ModelSerializer):

    def validate_progress(self, value):
        if value > 100:
            raise serializers.ValidationError("Прогресс не может быть больше 100%")
        elif value < 0:
            raise serializers.ValidationError("Прогресс не может быть меньше 0%")
        return value

    class Meta:
        model = IdeaInformation
        fields = ['id', 'progress', 'budget']


class CommentField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)

    def to_internal_value(self, data):
        try:
            uuid.UUID(data)
            return IdeaComment.objects.get(id=data)
        except ValueError:
            raise serializers.ValidationError("Invalid UUID")
        except IdeaComment.DoesNotExist:
            raise serializers.ValidationError("Comment does not exist")


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    children = serializers.SerializerMethodField()
    parent = CommentField(required=False, allow_null=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.author).data

    def get_children(self, obj):
        if self.context.get('parent', True):
            if obj.children.count() > 0:
                return CommentSerializer(obj.children.all(), many=True, context={'parent': False}).data
            else:
                return None
        return [] if obj.children.count() > 0 else None

    def create(self, validated_data):
        validated_data['idea'] = Idea.objects.get(id=self.context['kwargs'].get('idea_id'))
        validated_data['author'] = self.context['kwargs'].get('user')
        return super().create(validated_data)

    class Meta:
        model = IdeaComment
        fields = ['id', 'text', 'parent', 'children', 'created_at', 'updated_at', 'user']


class IdeaDocumentsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return f"https://{S3_IDEA_FILES_BUCKET}.{S3_SERVER}/{obj.path}"

    class Meta:
        model = IdeaDocument
        fields = ['id', 'url', 'created_at']


@dataclass
class File:
    file: str
    mime: str
    file_name: str
    file_size: int


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, data):
        file = data['file'] or data['image']

        data['mime'] = file.content_type
        data['file_name'] = file.name
        file_size = file.size
        if file_size > 50 * 1024 * 1024:
            raise ValidationError("Файл слишком большой. Загрузите файл меньше 50 Мб")
        data['file_size'] = file_size
        allowed_mime_types = self.context.get('allowed_mime_types')
        if allowed_mime_types and data['mime'] not in allowed_mime_types:
            raise ValidationError("Недопустимый формат файла")
        if isinstance(file, InMemoryUploadedFile):
            data['file'] = file.file
        elif isinstance(file, TemporaryUploadedFile):
            data['file'] = file.read()
        else:
            raise ValidationError("Файл слишком большой")
        return data

    def create(self, validated_data):
        return File(**validated_data)


class IdeaLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaLike
        fields = ['id', 'value', 'created_at']
