from django.urls import path

from core.vk_integration import VKCallbackView

urlpatterns = [
    path('vk/callback', VKCallbackView.as_view()),
]
