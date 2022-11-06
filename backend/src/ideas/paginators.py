from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from django.db.models.functions import Concat

from core.utils.http import Response
from ideas.posts.serializers import PostCommentSerializer
from ideas.serializers.serializers import BriefIdeaSerializer, CommentSerializer, IdeaCategorySerializer


def aux_ideas_paginator(ideas, search, page, items_per_page, sort_by, sort_desc, off_sort=False, kwargs=None):
    payload = ideas.distinct()

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
        if not off_sort:
            payload = payload.order_by('-created_at')
    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}

    has_next_page = page.has_next()
    payload = BriefIdeaSerializer(page, many=True, context={"kwargs": kwargs}).data

    return Response({"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
                     "payload": payload})


def aux_comments_paginator(comments, search, page, items_per_page, sort_by, sort_desc, post=False):
    payload = comments.distinct()

    if search:
        search = search.strip()
        payload.annotate(search=Concat('text', 'author__username', 'author__snp')).filter(
            search=search).distinct()
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value == 'created_at':
                payload = payload.order_by(f'{order_value}created_at')
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
    if not post:
        payload = CommentSerializer(page, many=True, context={'parent': True}).data
    else:
        payload = PostCommentSerializer(page, many=True, context={'parent': False}).data
    return Response({"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
                     "payload": payload})


def aux_category_paginator(categories, search, page, items_per_page, sort_by, sort_desc):
    payload = categories.annotate(ideas_count=Count('ideas')).distinct()

    if search:
        search = search.strip()
        payload.annotate(search=SearchVector('name', 'description')).filter(
            search=search).distinct()
    if sort_by:
        for sort_value, order_value in zip(sort_by, sort_desc):
            if sort_value == 'created_at':
                payload = payload.order_by(f'{order_value}created_at')
            elif sort_value == 'name':
                payload = payload.order_by(f'{order_value}name')
            else:
                payload = payload.order_by('-ideas_count')
    else:
        payload = payload.order_by('-ideas_count')
    paginator = Paginator(payload, items_per_page)
    total_pages = paginator.num_pages
    total_count = paginator.count

    try:
        page = paginator.page(page)
    except EmptyPage:
        return {"total_pages": total_pages, "total_count": total_count, "has_next_page": False, "payload": []}
    has_next_page = page.has_next()
    payload = IdeaCategorySerializer(page, many=True, context={'parent': False}).data
    return Response({"total_pages": total_pages, "total_count": total_count, "has_next_page": has_next_page,
                     "payload": payload})
