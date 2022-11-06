from django.contrib import admin

from iam.models import LogoutUser
from users.models import User, UserProfile, ProfileSettings, SocialNetwork, Skill, Interest, UserAddInfo, Country, \
    University, TeamRole


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'name', 'surname', 'patronymic', 'email', 'created_at', 'updated_at',
        'is_active')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'username', 'email']


admin.site.register(User, UserAdmin)


class LogoutUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'iat_before', 'logout_type', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ['id', 'user__id', 'session_id', 'user__short_id']


admin.site.register(LogoutUser, LogoutUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'sex', 'birthdate', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('skills', 'interests')


admin.site.register(UserProfile, UserProfileAdmin)


class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'show_birthdate', 'show_sex', 'show_biography', 'show_phone', 'show_email', 'show_social_networks',
        'show_skills', 'show_interests', 'can_be_invited')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_editable = ('show_birthdate', 'show_sex', 'show_biography', 'show_phone', 'show_email', 'show_social_networks',
                     'show_skills', 'show_interests', 'can_be_invited')


admin.site.register(ProfileSettings, ProfileSettingsAdmin)
admin.site.register(SocialNetwork)


class UserAddInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'citizenship', 'education_university', 'education_speciality', 'education_end_year', 'employment',
        'work_experience', 'has_iar', 'has_own_company', 'hack_experience', 'created_at', 'updated_at')


admin.site.register(UserAddInfo, UserAddInfoAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight', 'parent', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(Skill, SkillAdmin)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight', 'parent', 'chat', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(Interest, InterestAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_code', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(Country, CountryAdmin)


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(University, UniversityAdmin)


class TeamRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(TeamRole, TeamRoleAdmin)
