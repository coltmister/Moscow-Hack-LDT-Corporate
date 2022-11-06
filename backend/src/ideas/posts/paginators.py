from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage
from django.db.models.functions import Concat

from core.utils.http import Response
from ideas.posts.serializers import BriefPostSerializer, PostCommentSerializer


def aux_posts_paginator(posts, search, page, items_per_page, sort_by, sort_desc):
    payload = posts.distinct()

    if search:
        search = search.strip()
        filter_temp = SearchVector('title', 'description', 'author__username')
        payload = payload.annotate(search=filter_temp).filter(
            search=search).distinct()
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value == 'created_at':
                payload = payload.order_by(f'{order_value}created_at')
            elif sort_value == 'title':
                payload = payload.order_by(f'{order_value}title')
            elif sort_value == 'author':
                payload = payload.order_by(f'{order_value}author__snp')
            else:
                payload = payload.order_by('-created_at')
    else:
        payload = payload.order_by('-created_at')
    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    has_next_page = page.has_next()
    payload = BriefPostSerializer(page, many=True).data

    return Response({"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
                     "payload": payload})
