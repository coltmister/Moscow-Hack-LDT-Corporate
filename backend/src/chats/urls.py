from django.urls import path

from chats.views import ChatNotificationsView, ChatsView, VKChatInviteLinkView, CreateInterestChat

urlpatterns = [
    path('', ChatsView.as_view()),
    path('<uuid:chat_pk>', ChatsView.as_view()),
    path('notifications', ChatNotificationsView.as_view()),
    path('notifications/chat/<uuid:chat_pk>', ChatNotificationsView.as_view()),
    path('notifications/<uuid:notification_pk>', ChatNotificationsView.as_view()),
    path('teams/<uuid:team_pk>/vk-chat', VKChatInviteLinkView.as_view()),
    path('interests/<uuid:interest_pk>/vk-chat', CreateInterestChat.as_view()),
]
