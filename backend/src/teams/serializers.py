from rest_framework import serializers
from rest_framework.fields import UUIDField

from chats.serializers import ChatSerializer
from chats.views import create_vk_team_chat
from ideas.models import Idea
from ideas.serializers.serializers import BriefIdeaSerializer
from teams.models import Team, TeamRequest, Membership, RequiredMembers
from users.models import User, TeamRole
from users.serializers import UserSerializer, TeamRoleSerializer


class BriefTeamSerializer(serializers.ModelSerializer):
    team_leader = UserSerializer()
    idea = serializers.SerializerMethodField()

    def get_idea(self, obj):
        return {
            "id": str(obj.idea.id),
            "title": obj.idea.title,
        }

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'team_leader', 'is_looking_for_members', 'idea']


class WriteMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'team', 'role', 'date_joined', 'membership_requester']
        extra_kwargs = {
            'team': {'required': False, 'allow_null': True},
            'membership_requester': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        validated_data['team'] = self.context.get('team')
        validated_data['membership_requester'] = Membership.ADMINISTRATOR
        return super().create(validated_data)


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = TeamRoleSerializer()
    membership_requester = serializers.SerializerMethodField()

    def get_membership_requester(self, obj):
        membership_requester = {
            "id": obj.membership_requester,
            "name": obj.get_membership_requester_display()
        }
        return membership_requester

    class Meta:
        model = Membership
        fields = ['user', 'role', 'date_joined', 'membership_requester']


class RequiredMembersSerializer(serializers.Serializer):
    role = serializers.PrimaryKeyRelatedField(queryset=TeamRole.objects.all(), pk_field=UUIDField(format='hex_verbose'))
    amount = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'role': {
                "id": str(instance.role.id),
                "name": instance.role.name
            },
            'amount': instance.amount
        }


class TeamSerializer(serializers.ModelSerializer):
    idea = BriefIdeaSerializer()
    members = serializers.SerializerMethodField()
    team_leader = UserSerializer()
    required_members = serializers.SerializerMethodField()
    chat = serializers.SerializerMethodField()

    def get_members(self, obj):
        members = Membership.objects.filter(team=obj)
        return MembershipSerializer(members, many=True).data

    def get_required_members(self, obj):
        required_members = RequiredMembers.objects.filter(team=obj)
        return RequiredMembersSerializer(required_members, many=True).data

    def get_chat(self, obj):
        # Возвращаю чат в ВК
        current_user = self.context.get('current_user')
        if not (obj.team_leader == current_user or current_user in obj.members.all()):
            return None
        return ChatSerializer(obj.chat).data

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'idea', 'members', 'required_members', 'team_leader',
                  'is_looking_for_members', 'chat']


class WriteTeamSerializer(serializers.ModelSerializer):
    idea = serializers.PrimaryKeyRelatedField(queryset=Idea.objects.all(),
                                              pk_field=UUIDField(format='hex_verbose'),
                                              required=False,
                                              allow_null=True)
    team_leader = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                     pk_field=UUIDField(format='hex_verbose'),
                                                     required=False,
                                                     allow_null=True)
    required_members = RequiredMembersSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'idea', 'team_leader', 'is_looking_for_members', 'required_members']

    def validate(self, data):
        current_user = self.context.get('user')
        idea = data.get('idea')
        if not self.instance:
            if not idea:
                raise serializers.ValidationError('Вы не выбрали идею')
            if not idea.author == current_user:
                raise serializers.ValidationError('Вы не являетесь автором идеи и не можете создать команду для нее')
            if Team.objects.filter(idea=idea).exists():
                raise serializers.ValidationError('Команда для этой идеи уже существует')
        else:
            if not (current_user == self.instance.team_leader or current_user.is_admin):
                raise serializers.ValidationError('Вы не являетесь лидером команды и не можете изменить ее')

            if idea and idea != self.instance.idea:
                raise serializers.ValidationError('Вы не можете изменить идею команды')
        return data

    def create(self, validated_data):
        required_members = validated_data.pop('required_members')
        team = super().create(validated_data)
        team.members.add(self.context.get('user'), through_defaults={'role': None,
                                                                     'membership_requester': Membership.AUTOMATIC})
        if required_members:
            team.required_members.clear()
            for member in required_members:
                role = member.get('role')
                amount = member.get('amount')
                team.required_members.add(role, through_defaults={'amount': amount})

        # Создание чата в ВК
        create_vk_team_chat.apply_async(kwargs={"team_pk": str(team.id)})

        return team

    def update(self, instance, validated_data):
        validated_data.pop('idea', None)
        validated_data.pop('team_leader', None)
        required_members = validated_data.pop('required_members')
        instance = super().update(instance, validated_data)
        if required_members:
            instance.required_members.clear()
            for member in required_members:
                role = member.get('role')
                amount = member.get('amount')
                instance.required_members.add(role, through_defaults={'amount': amount})
        return instance


class WriteUserOutgoingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequest
        fields = ['id', 'team', 'user', 'role', 'request_type', 'cover_letter', 'request_status']
        extra_kwargs = {"user": {"allow_null": True, "required": False},
                        "request_status": {"allow_null": True, "required": False},
                        "request_type": {"allow_null": True, "required": False}}

    def validate(self, data):
        current_user = self.context.get('user')
        team = data.get('team')
        data['request_type'] = TeamRequest.OUTGOING
        if not self.instance:
            if current_user in team.members.all() or current_user == team.team_leader:
                raise serializers.ValidationError('Вы уже состоите в этой команде')
            if not team.is_looking_for_members:
                raise serializers.ValidationError('Эта команда не ищет новых участников')

            if TeamRequest.objects.filter(team=team, user=current_user, request_type=TeamRequest.OUTGOING).exists():
                raise serializers.ValidationError('Вы уже отправили запрос на вступление в эту команду')
        else:
            if not current_user == self.instance.user:
                raise serializers.ValidationError('Вы не можете изменить чужой запрос')
        return data


class WriteTeamOutgoingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequest
        fields = ['id', 'team', 'user', 'role', 'request_type', 'cover_letter', 'request_status']
        extra_kwargs = {"team": {"allow_null": True, "required": False},
                        "request_status": {"allow_null": True, "required": False},
                        "request_type": {"allow_null": True, "required": False}}

    def validate(self, data):
        current_user = self.context.get('user')
        invited_user = data.get('user')
        team = self.context.get('team') or data.get('team')
        if not team:
            raise serializers.ValidationError('Команда не найдена')
        data['team'] = team
        data['request_type'] = TeamRequest.INCOMING
        if not self.instance:
            if current_user != team.team_leader:
                raise serializers.ValidationError(
                    'Вы не являетесь лидером команды и не можете приглашать пользователей')
            if invited_user in team.members.all() or invited_user == team.team_leader:
                raise serializers.ValidationError('Приглашаемый пользователь уже состоит в этой команде')
            if not invited_user.profile.profile_settings.can_be_invited:
                raise serializers.ValidationError(
                    'Приглашаемый пользователь заблокировал в настройках получение приглашений')
            if not team.is_looking_for_members:
                raise serializers.ValidationError('Ваша команда в данный момент не ищет новых участников')

            if TeamRequest.objects.filter(team=team, user=invited_user, request_type=TeamRequest.INCOMING).exists():
                raise serializers.ValidationError('Вы уже отправили запрос на приглашение этого пользователя')

        return data


class RequestSerializer(serializers.ModelSerializer):
    team = BriefTeamSerializer()
    user = UserSerializer()
    role = TeamRoleSerializer()
    request_status = serializers.SerializerMethodField()

    def get_request_status(self, obj):
        return {
            "id": [x[0] for x in TeamRequest.REQUEST_STATUS].index(obj.request_status),
            "name": obj.get_request_status_display()
        }

    class Meta:
        model = TeamRequest
        fields = ['id', 'team', 'user', 'role', 'cover_letter', 'request_status']
