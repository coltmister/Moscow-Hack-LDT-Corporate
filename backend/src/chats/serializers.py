from rest_framework import serializers

from chats.models import Chat, ChatNotification



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'chat_link', 'chat_id', 'chat_type', 'peer_id', 'users_count']


class ChatNotificationSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()

    class Meta:
        model = ChatNotification
        fields = ['id', 'chat', 'message', 'is_read']
