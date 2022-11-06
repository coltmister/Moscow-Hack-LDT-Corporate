from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import UUIDField
from rest_framework.relations import PrimaryKeyRelatedField

from chats.serializers import ChatSerializer
from users.models import User, UserProfile, SocialNetwork, ProfileSettings, Skill, Interest, UserAddInfo, Country, \
    University, TeamRole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'surname', 'patronymic', 'is_active', 'is_admin', 'is_verified', 'snp',
                  'avatar',
                  'avatar_thumbnail']


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ['id', 'network_type', 'nickname']

    def validate(self, data):
        network_type = data.get('network_type')
        nickname = data.get('nickname')
        if SocialNetwork.objects.filter(network_type=network_type, nickname=nickname).exists():
            raise serializers.ValidationError(
                f"Аккаунт в {network_type} c именем {nickname} уже привязан к другому пользователю")
        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'parent']


class InterestSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()
    parent = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), pk_field=UUIDField(format='hex_verbose'))

    class Meta:
        model = Interest
        fields = ['id', 'name', 'parent', 'chat']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'status', 'avatar', 'avatar_thumbnail', 'biography', 'phone', 'birthdate', 'sex',
                  'skills', 'interests']

    def validate(self, data):
        data.pop('user', None)
        data.pop('avatar', None)
        data.pop('avatar_thumbnail', None)
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.sex == UserProfile.MALE:
            sex_name = 'Мужской'
        elif instance.sex == UserProfile.FEMALE:
            sex_name = 'Женский'
        else:
            sex_name = 'Не указан'

        representation['sex'] = {
            "id": representation['sex'],
            "name": sex_name
        }
        representation['social_networks'] = SocialNetworkSerializer(instance.social_networks, many=True).data
        representation['skills'] = SkillSerializer(instance.skills, many=True).data
        representation['interests'] = InterestSerializer(instance.interests, many=True).data

        if not self.context.get('me'):
            representation['email'] = instance.user.email if instance.profile_settings.show_email else None
            representation['phone'] = instance.phone if instance.profile_settings.show_phone else None
            representation['birthdate'] = str(instance.birthdate) if instance.profile_settings.show_birthdate else None
            representation['sex'] = instance.sex if instance.profile_settings.show_sex else None
            representation['biography'] = instance.biography if instance.profile_settings.show_biography else None
            representation['social_networks'] = representation[
                'social_networks'] if instance.profile_settings.show_social_networks else []

            representation['skills'] = representation[
                'skills'] if instance.profile_settings.show_skills else []
            representation['interests'] = representation[
                'interests'] if instance.profile_settings.show_interests else []

        else:
            # Если пользователь запрашивает свой профиль, то он должен видеть все данные
            representation['email'] = instance.user.email
        return representation

    def to_internal_value(self, data):
        social_networks = data.pop('social_networks', [])
        data = super().to_internal_value(data)
        data['social_networks'] = social_networks
        return data

    def update(self, instance, validated_data):
        social_networks = validated_data.pop('social_networks', [])
        # Обновляем профиль
        instance = super().update(instance, validated_data)
        existed_social_networks = set([str(social_network_id) for social_network_id in
                                       instance.social_networks.all().values_list('id', flat=True)])
        new_social_networks = set()
        with transaction.atomic():
            for social_network in social_networks:
                if "id" in social_network:
                    # Обновляем
                    social_network_id = social_network['id']
                    SocialNetwork.objects.filter(id=social_network_id, user_profile=instance).update(**social_network)
                else:
                    # Создаем
                    serializer = SocialNetworkSerializer(data=social_network)
                    serializer.is_valid(raise_exception=True)
                    social_network_id = serializer.save(user_profile=instance).id
                new_social_networks.add(social_network_id)
            # Удаляем
            social_networks_to_delete = existed_social_networks - new_social_networks
            SocialNetwork.objects.filter(id__in=social_networks_to_delete).delete()

        return instance


class UserProfileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSettings
        fields = ['id', 'show_birthdate', 'show_sex', 'show_biography', 'show_phone', 'show_email',
                  'show_social_networks', 'show_skills', 'show_interests', 'can_be_invited',
                  'show_citizenship', 'show_education', 'show_employment', 'show_work_experience',
                  'show_professional_experience', 'show_team_roles', 'show_iar_information', 'show_company_information',
                  'show_hack_experience']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name']


class TeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRole
        fields = ['id', 'name']


class UserAddInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    citizenship = CountrySerializer()
    education_university = UniversitySerializer()
    team_role = TeamRoleSerializer(many=True)
    education_level = serializers.SerializerMethodField()
    employment = serializers.SerializerMethodField()

    def get_education_level(self, instance):
        education_level = {
            "id": instance.education_level,
            "name": instance.get_education_level_display()
        }
        return education_level

    def get_employment(self, instance):
        employment = {
            "id": instance.employment,
            "name": instance.get_employment_display()
        }
        return employment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context.get('me'):
            if not instance.user.profile.profile_settings.show_citizenship:
                representation['citizenship'] = None
            if not instance.user.profile.profile_settings.show_education:
                representation['education_university'] = None
                representation['education_level'] = None
                representation['education_speciality'] = None
                representation['education_end_year'] = None
            if not instance.user.profile.profile_settings.show_employment:
                representation['employment'] = None
            if not instance.user.profile.profile_settings.show_work_experience:
                representation['work_experience'] = None
            if not instance.user.profile.profile_settings.show_professional_experience:
                representation['professional_experience'] = None
            if not instance.user.profile.profile_settings.show_team_roles:
                representation['team_role'] = []
            if not instance.user.profile.profile_settings.show_iar_information:
                representation['has_iar'] = None
            if not instance.user.profile.profile_settings.show_company_information:
                representation['has_own_company'] = None
            if not instance.user.profile.profile_settings.show_hack_experience:
                representation['hack_experience'] = None

        return representation

    class Meta:
        model = UserAddInfo
        fields = ['id', 'user', 'citizenship', 'education_university', 'education_level', 'education_speciality',
                  'education_end_year',
                  'employment', 'work_experience', 'professional_experience', 'team_role', 'has_iar', 'has_own_company',
                  'hack_experience']


class WriteUserAddInfoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              pk_field=UUIDField(format='hex_verbose'),
                                              required=False,
                                              allow_null=True)
    citizenship = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                     pk_field=UUIDField(format='hex_verbose'),
                                                     required=False,
                                                     allow_null=True)
    education_university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(),
                                                              pk_field=UUIDField(format='hex_verbose'),
                                                              required=False,
                                                              allow_null=True)
    team_role = serializers.PrimaryKeyRelatedField(queryset=TeamRole.objects.all(),
                                                   pk_field=UUIDField(format='hex_verbose'),
                                                   required=False,
                                                   allow_null=True,
                                                   many=True)

    class Meta:
        model = UserAddInfo
        fields = ['id', 'user', 'citizenship', 'education_university', 'education_level', 'education_speciality',
                  'education_end_year',
                  'employment', 'work_experience', 'professional_experience', 'team_role', 'has_iar', 'has_own_company',
                  'hack_experience']

    def update(self, instance, validated_data):
        # Обновляем профиль
        instance = super().update(instance, validated_data)

        return instance


class ExtendedUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    add_info = UserAddInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'surname', 'patronymic', 'is_active', 'is_admin', 'is_verified', 'snp',
                  'avatar', 'avatar_thumbnail', 'profile', 'add_info']
