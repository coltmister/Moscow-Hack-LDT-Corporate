import logging

from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action
from core.utils.http import Response
from users.models import Skill, Interest, Country, University, TeamRole
from users.serializers import SkillSerializer, \
    InterestSerializer, CountrySerializer, UniversitySerializer, TeamRoleSerializer

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class SkillsView(APIView):
    """Просмотр списка навыков"""

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            skills = Skill.objects.filter(name__icontains=search)
        else:
            skills = Skill.objects.all()
        return Response(SkillSerializer(skills, many=True).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class InterestsView(APIView):
    """Просмотр списка интересов"""

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            interests = Interest.objects.filter(name__icontains=search)
        else:
            interests = Interest.objects.all()

        return Response(InterestSerializer(interests, many=True).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class CountryView(APIView):
    """Просмотр списка стран"""

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            countries = Country.objects.filter(name__icontains=search)
        else:
            countries = Country.objects.all()
        return Response(CountrySerializer(countries, many=True).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UniversityView(APIView):
    """Просмотр списка университетов"""

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            universities = University.objects.filter(name__icontains=search)
        else:
            universities = University.objects.all()
        return Response(UniversitySerializer(universities, many=True).data)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class TeamRoleView(APIView):
    """Просмотр списка ролей в команде"""

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            team_roles = TeamRole.objects.filter(name__icontains=search)
        else:
            team_roles = TeamRole.objects.all()
        return Response(TeamRoleSerializer(team_roles, many=True).data)
