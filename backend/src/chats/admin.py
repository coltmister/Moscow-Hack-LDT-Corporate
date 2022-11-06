from django.contrib import admin

from chats.models import Chat, ChatNotification


# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'chat_link', 'chat_id', 'peer_id', 'users_count', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(Chat, ChatAdmin)


class ChatNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'message', 'is_read', 'created_at', 'updated_at']
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ['id', 'name']


admin.site.register(ChatNotification, ChatNotificationAdmin)
