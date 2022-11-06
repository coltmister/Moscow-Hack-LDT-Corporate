from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, QuerySet

from teams.models import Team
from teams.rating import team_rating
from teams.serializers import TeamSerializer


def team_paginator(users: QuerySet, search: str, page: int, items_per_page: int, sort_by: str, sort_desc: str,
                   current_user):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(name__icontains=word) | Q(description__icontains=word) | Q(
                idea__title__icontains=word) | Q(idea__description__icontains=word) | Q(
                team_leader__profile__skills__name__icontains=word) | Q(members__profile__skills__name__icontains=word)
        payload = payload.filter(payload_search)

    model_fields = [field.name for field in Team._meta.get_fields()]
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
    payload = TeamSerializer(instance=page, many=True, context={"current_user": current_user}).data
    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}


def team_vacancy_paginator(users: QuerySet, less_suitable_teams: QuerySet, search: str, page: int, items_per_page: int,
                           sort_by: str, sort_desc: str, current_user):
    payload = users.distinct()
    if search:
        payload_search = Q()
        splited_search = search.split()
        for word in splited_search:
            payload_search &= Q(name__icontains=word) | Q(description__icontains=word) | Q(
                idea__title__icontains=word) | Q(idea__description__icontains=word) | Q(
                team_leader__profile__skills__name__icontains=word) | Q(members__profile__skills__name__icontains=word)
        payload = payload.filter(payload_search)

    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    try:
        suitable_teams = sorted(page, key=team_rating, reverse=True)
    except Exception:
        suitable_teams = page

    has_next_page = page.has_next()
    payload = TeamSerializer(instance=suitable_teams, many=True, context={"current_user": current_user}).data
    return {"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
            "payload": payload}
