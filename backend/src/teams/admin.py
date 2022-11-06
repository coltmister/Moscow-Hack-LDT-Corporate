from django.contrib import admin

from teams.models import Team, TeamRequest, Membership, RequiredMembers


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1  # choose any number


class RequiredMembersInline(admin.TabularInline):
    model = RequiredMembers
    extra = 1  # choose any number


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'team_leader', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ['id', 'name', 'description']
    inlines = [MembershipInline, RequiredMembersInline]


admin.site.register(Team, TeamAdmin)


class TeamRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'team', 'user', 'request_type', 'request_status', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ['id', 'team__id', 'user__id']


admin.site.register(TeamRequest, TeamRequestAdmin)
