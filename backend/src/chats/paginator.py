from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, QuerySet

from chats.models import ChatNotification, Chat
from chats.serializers import ChatNotificationSerializer, ChatSerializer


def chat_notification_paginator(users: QuerySet, search: str, page: int, items_per_page: int, sort_by: str,
                                sort_desc: str):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(text__icontains=word)
        payload = payload.filter(payload_search)

    model_fields = [field.name for field in ChatNotification._meta.get_fields()]
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value in model_fields:
                payload = payload.order_by(f'{order_value}{sort_value}')
    else:
        payload = payload.order_by('-id')

    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    has_next_page = page.has_next()
    payload = ChatNotificationSerializer(instance=page, many=True).data
    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}


def chat_paginator(users: QuerySet, search: str, page: int, items_per_page: int, sort_by: str,
                   sort_desc: str):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(name__icontains=word, chat_link__icontains=word)
        payload = payload.filter(payload_search)

    model_fields = [field.name for field in Chat._meta.get_fields()]
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value in model_fields:
                payload = payload.order_by(f'{order_value}{sort_value}')
    else:
        payload = payload.order_by('-id')

    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    has_next_page = page.has_next()
    payload = ChatSerializer(instance=page, many=True).data
    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}
