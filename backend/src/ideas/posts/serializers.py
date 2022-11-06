import uuid

from rest_framework import serializers

from ideas.models import Post, PostComment, PostLike, PostDocument
from ideas.serializers.serializers import UserSerializer, BriefIdeaSerializer
from settings.settings import S3_SERVER, S3_POST_FILES_BUCKET
from users.models import User


class PostCommentField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)

    def to_internal_value(self, data):
        try:
            uuid.UUID(data)
            return PostComment.objects.get(id=data)
        except ValueError:
            raise serializers.ValidationError("Invalid UUID")
        except PostComment.DoesNotExist:
            raise serializers.ValidationError("Comment does not exist")


class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', read_only=True)
    children = serializers.SerializerMethodField()
    parent = PostCommentField(required=False, allow_null=True)

    def get_children(self, obj):
        if self.context.get('parent', True):
            if obj.children.count() > 0:
                return PostCommentSerializer(obj.children.all(), many=True, context={'parent': False}).data
            else:
                return None
        return [] if obj.children.count() > 0 else None

    def create(self, validated_data):
        validated_data['post'] = Post.objects.get(id=self.context['kwargs'].get('post_id'))
        validated_data['author'] = self.context['kwargs'].get('user')
        return super().create(validated_data)

    class Meta:
        model = PostComment
        fields = ['id', 'text', 'parent', 'children', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)
    idea = BriefIdeaSerializer(read_only=True)
    my_reaction = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'idea', 'description', 'post_json', 'author', 'rating', 'comments', 'created_at',
            'updated_at',
            'my_reaction', 'reactions')

    def get_my_reaction(self, obj):
        kwargs = self.context.get('kwargs')
        user = None
        if kwargs:
            user = self.context.get('kwargs').get('user')
        if user:
            try:
                like = PostLike.objects.get(post=obj, author=user)
                return PostLikeSerializer(like).data
            except (ValueError, PostLike.DoesNotExist):
                return None
        return None

    def get_reactions(self, obj):
        likes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.LIKE).distinct()
        dislikes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.DISLIKE).distinct()
        super_likes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.SUPER_LIKE).distinct()
        neutrals = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.NEUTRAL).distinct()
        super_dislikes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.SUPER_DISLIKE).distinct()
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


class BriefPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    idea = BriefIdeaSerializer(read_only=True)
    my_reaction = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'idea', 'description', 'post_json', 'author', 'rating', 'created_at', 'updated_at',
                  'my_reaction', 'reactions')

    def get_my_reaction(self, obj):
        kwargs = self.context.get('kwargs')
        user = None
        if kwargs:
            user = self.context.get('kwargs').get('user')
        if user:
            try:
                like = PostLike.objects.get(post=obj, author=user)
                return PostLikeSerializer(like).data
            except (ValueError, PostLike.DoesNotExist):
                return None
        return None

    def get_reactions(self, obj):
        likes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.LIKE).distinct()
        dislikes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.DISLIKE).distinct()
        super_likes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.SUPER_LIKE).distinct()
        neutrals = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.NEUTRAL).distinct()
        super_dislikes = User.objects.filter(post_likes__post=obj, post_likes__value=PostLike.SUPER_DISLIKE).distinct()
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


class WritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'idea', 'description', 'post_json')

    def create(self, validated_data):
        validated_data['author'] = self.context['kwargs'].get('user')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['author'] = self.context['kwargs'].get('user')
        return super().update(instance, validated_data)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'value', 'created_at']


class PostDocumentsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return f"https://{S3_POST_FILES_BUCKET}.{S3_SERVER}/{obj.path}"

    class Meta:
        model = PostDocument
        fields = ['id', 'url', 'created_at']
