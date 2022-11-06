from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Value, QuerySet
from django.db.models.functions import Concat

from teams.rating import user_rating
from users.models import User
from users.serializers import UserSerializer, ExtendedUserSerializer


def user_paginator(users: QuerySet, search: str, page: int, items_per_page: int, sort_by: str, sort_desc: str):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(full_name__icontains=word) | Q(username__icontains=word)
        payload = payload.annotate(full_name=Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')).filter(
            payload_search).distinct()

    model_fields = [field.name for field in User._meta.get_fields()]
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value in model_fields:
                payload = payload.order_by(f'{order_value}{sort_value}')
            elif sort_value == 'snp':
                payload = payload.order_by(f'{order_value}surname', f'{order_value}name', f'{order_value}patronymic')
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
    payload = UserSerializer(instance=page, many=True).data

    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}


def extended_user_paginator(users: QuerySet,
                            search: str,
                            page: int,
                            items_per_page: int,
                            sort_by: str,
                            sort_desc: str):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(full_name__icontains=word) | Q(username__icontains=word)
        payload = payload.annotate(full_name=Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')).filter(
            payload_search).distinct()

    model_fields = [field.name for field in User._meta.get_fields()]
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value in model_fields:
                payload = payload.order_by(f'{order_value}{sort_value}')
            elif sort_value == 'snp':
                payload = payload.order_by(f'{order_value}surname', f'{order_value}name', f'{order_value}patronymic')
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
    payload = ExtendedUserSerializer(instance=page, many=True).data

    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}


def user_vacancy_extended_paginator(users: QuerySet, less_suitable_users: QuerySet, search: str, page: int,
                                    items_per_page: int, sort_by: str,
                                    sort_desc: str):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(full_name__icontains=word) | Q(username__icontains=word)
        payload = payload.annotate(full_name=Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')).filter(
            payload_search).distinct()

    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    try:
        suitable_users = sorted(page, key=user_rating, reverse=True)
    except Exception:
        suitable_users = page

    has_next_page = page.has_next()
    payload = ExtendedUserSerializer(instance=suitable_users, many=True).data

    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}
