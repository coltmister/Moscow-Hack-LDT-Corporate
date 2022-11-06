import logging

from django.db.models import Count
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action
from core.utils.exceptions import BadRequestException
from core.utils.http import clean_get_params, Response
from ideas.models import Idea
from ideas.paginators import aux_ideas_paginator
from users.models import User

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class FeedIdeaView(APIView):
    def __init__(self):
        super().__init__()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_new_ideas(self, get_params=None, kwargs=None):
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).order_by('-created_at')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get_popular_ideas(self, get_params=None, kwargs=None):
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).annotate(
            comment_count=Count('comments')).order_by(
            '-comment_count')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get_ideas_by_tags(self, user: User, get_params=None, kwargs=None):
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).filter(
            tags__in=user.profile.interests.all()).order_by(
            '-created_at')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get_people_choice_ideas(self, get_params=None, kwargs=None):
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).order_by('-rating')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get_smart_ideas(self, user: User, get_params=None, kwargs=None):
        user_likes = user.likes.all()
        user_ideas = [like.idea for like in user_likes]
        user_tags = [tag for idea in user_ideas for tag in idea.tags.all()]
        like_tags = {i: user_tags.count(i) for i in user_tags}
        top_tags = sorted(like_tags.items(), key=lambda x: x[1], reverse=True)[:3]
        top_tags = [tag[0] for tag in top_tags]
        user_tags = [tag for tag in user_tags if tag not in top_tags]
        top_tags.extend(user_tags)
        top_tags = top_tags[:3]
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).filter(
            tags__in=top_tags).order_by(
            '-rating')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get_sandbox_ideas(self, get_params=None, kwargs=None):
        ideas = Idea.objects.filter(status__in=[Idea.STATUS_APPROVED, Idea.STATUS_FINISHED]).order_by('-created_at')
        return aux_ideas_paginator(ideas, *get_params, off_sort=True, kwargs=kwargs)

    def get(self, request, *args, **kwargs):
        feed_param = request.GET.get('feed_param')
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)
        if feed_param is None:
            raise BadRequestException('Необходимо указать параметр feed')
        if feed_param == "new":
            return self.get_new_ideas(get_params, kwargs)
        elif feed_param == "popular":
            return self.get_popular_ideas(get_params, kwargs)
        elif feed_param == "my_tags":
            return self.get_ideas_by_tags(kwargs.get('user'), get_params, kwargs)
        elif feed_param == "smart":
            return self.get_smart_ideas(kwargs.get('user'), get_params, kwargs)
        elif feed_param == "people_choice":
            return self.get_people_choice_ideas(get_params, kwargs)
        elif feed_param == "sandbox":
            return self.get_sandbox_ideas(get_params, kwargs)
        else:
            raise BadRequestException('Неверный параметр feed')
