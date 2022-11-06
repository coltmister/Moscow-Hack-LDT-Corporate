import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from core.utils.decorators import tryexcept, auth, log_action, admin_only
from core.utils.email import send_email
from core.utils.exceptions import BadRequestException
from core.utils.http import clean_get_params, Response
from teams.models import Team, TeamRequest, Membership
from teams.paginator import team_paginator, team_vacancy_paginator
from teams.rating import does_team_need_this_user
from teams.serializers import TeamSerializer, WriteTeamSerializer, WriteUserOutgoingRequestSerializer, \
    RequestSerializer, WriteTeamOutgoingRequestSerializer, WriteMembershipSerializer
from users.models import User, TeamRole
from users.paginator import user_vacancy_extended_paginator

logger = logging.getLogger(__name__)


@method_decorator([tryexcept, auth, admin_only, log_action], name='dispatch')
class AddUserToTeamView(APIView):
    def post(self, request, team_pk, *args, **kwargs):
        """Добавить пользователя в команду от имени администратора"""
        try:
            team = Team.objects.get(pk=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content='Команда не найдена')
        serializer = WriteMembershipSerializer(data=request.data, context={'team': team})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class TeamView(APIView):
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, team_pk=None, *args, **kwargs):
        """Просмотр всех пользователей или заданного пользователя"""

        if not team_pk:
            teams = Team.objects.all()
            try:
                get_params = clean_get_params(request)
            except BadRequestException as error:
                return Response(status=400, content=error.message)
            return Response(team_paginator(teams, *get_params, current_user=self.user))

        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        serializer = TeamSerializer(instance=team, context={'current_user': self.user})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Создание команды"""
        serializer = WriteTeamSerializer(data=request.data, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(team_leader=self.user)
        return Response(status=201, content={"id": str(data.id)})

    def put(self, request, team_pk, *args, **kwargs):
        """Редактирование команды"""
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")
        serializer = WriteTeamSerializer(instance=team, data=request.data, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def delete(self, request, team_pk, *args, **kwargs):
        """Удаление команды"""
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if not (self.user == team.team_leader or self.user.is_admin):
            return Response(status=400, content="Вы не можете удалить чужую команду")

        team.delete()
        return Response(status=200)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class KickUserFromTeamView(APIView):
    def delete(self, request, team_pk, user_pk, *args, **kwargs):
        """Исключить человека из беседы"""
        current_user = kwargs.get('user')
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if not (current_user == team.team_leader or current_user.is_admin):
            return Response(status=400, content="Вы не можете исключить человека из чужой команды")

        try:
            user = User.objects.get(id=user_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Пользователь не найден")

        if user == team.team_leader:
            return Response(status=400, content="Нельзя исключить лидера команды")

        team.members.remove(user)
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class SetUserTeamRole(APIView):
    def put(self, request, team_pk, user_pk, *args, **kwargs):
        """Изменить роль пользователя в команде"""
        current_user = kwargs.get('user')
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if not (current_user == team.team_leader or current_user.is_admin):
            return Response(status=400, content="Вы не можете изменить роль в чужой команде")

        try:
            user = User.objects.get(id=user_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Пользователь не найден")

        try:
            membership = Membership.objects.get(team=team, user=user)
        except ObjectDoesNotExist:
            return Response(status=404, content="Пользователь не состоит в команде")

        role = request.data.get('role')
        try:
            role = TeamRole.objects.get(id=role)
        except ObjectDoesNotExist:
            return Response(status=404, content="Роль не найдена")
        membership.role = role
        membership.save()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class LeaveTeamView(APIView):
    def delete(self, request, team_pk, *args, **kwargs):
        """Выход из команды"""
        current_user = kwargs.get('user')
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if current_user == team.team_leader:
            return Response(status=400, content="Нельзя выйти из команды, если вы лидер")

        team.members.remove(current_user)
        # TODO Отправлять сообщение тимлиду о том, что пользователь покинул команду
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserOutgoingRequestView(APIView):
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Просмотр всех исходящих запросов пользователя"""
        request_status = request.GET.get('request_status', None)
        outgoing_requests = self.user.user_requests.filter(request_type=TeamRequest.OUTGOING)
        if request_status:
            outgoing_requests = outgoing_requests.filter(request_status=request_status)
        serializer = RequestSerializer(instance=outgoing_requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Создать пользователем запрос на вступление в команду"""
        serializer = WriteUserOutgoingRequestSerializer(data=request.data, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(user=self.user)

        main_text = f"""Пользователь {self.user.snp} желает вступить в вашу команду '{data.team.name}'"""
        email_data = {
            "receivers": [data.team.team_leader.email],
            "subject": "Уведомление на платформе Σ | Эврика",
            "title": "Новый запрос на вступление в команду",
            "greeting": f"Здравствуйте, {data.team.team_leader.get_greeting_name()}!",
            "main_text": main_text,
            "bottom_text": None,
            "button_text": None,
            "button_link": None
        }

        send_email.apply_async(kwargs={"email_data": email_data})

        return Response(status=201, content={"id": str(data.id)})

    def delete(self, request, request_pk, *args, **kwargs):
        """Удалить запрос на вступление в команду"""
        try:
            outgoing_request = TeamRequest.objects.get(id=request_pk,
                                                       user=self.user,
                                                       request_type=TeamRequest.OUTGOING,
                                                       request_status=TeamRequest.REQUEST_SUBMITTED)
        except ObjectDoesNotExist:
            return Response(status=404, content="Активный запрос не найден")

        outgoing_request.delete()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserIncomingRequestView(APIView):
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Просмотр входящих запросов"""
        request_status = request.GET.get('request_status', None)
        incoming_requests = self.user.user_requests.filter(request_type=TeamRequest.INCOMING)
        if request_status:
            incoming_requests = incoming_requests.filter(request_status=request_status)
        serializer = RequestSerializer(instance=incoming_requests, many=True)
        return Response(serializer.data)

    def put(self, request, request_pk, *args, **kwargs):

        """Принятие или отклонение входящей заявки о приглащении в команду"""
        try:
            incoming_request = TeamRequest.objects.get(id=request_pk,
                                                       request_type=TeamRequest.INCOMING,
                                                       request_status=TeamRequest.REQUEST_SUBMITTED)
        except ObjectDoesNotExist:
            return Response(status=404, content="Запрос не найден")

        decision = request.data.get('decision', None)
        if decision is None:
            return Response(status=400, content="Не указано решение")
        if decision:
            incoming_request.request_status = TeamRequest.REQUEST_ACCEPTED
            incoming_request.save()
            incoming_request.team.members.add(self.user, through_defaults={'role': incoming_request.role,
                                                                           'membership_requester': Membership.TEAM})

            main_text = f"""Пользователь {self.user.snp} принял ваше приглашение о вступлении в команду '{incoming_request.team.name}'"""
            email_data = {
                "receivers": [incoming_request.team.team_leader.email],
                "subject": "Уведомление на платформе Σ | Эврика",
                "title": "В Вашей команде пополнение!",
                "greeting": f"Здравствуйте, {incoming_request.team.team_leader.get_greeting_name()}!",
                "main_text": main_text,
                "bottom_text": None,
                "button_text": None,
                "button_link": None
            }

            send_email.apply_async(kwargs={"email_data": email_data})

            return Response(status=204, content=f"Вы вступили в команду {incoming_request.team.name}")
        else:
            incoming_request.request_status = TeamRequest.REQUEST_DECLINED
            incoming_request.save()

            main_text = f"""Пользователь {self.user.snp} отклонил ваше приглашение о вступлении в команду '{incoming_request.team.name}'"""
            email_data = {
                "receivers": [incoming_request.team.team_leader.email],
                "subject": "Уведомление на платформе Σ | Эврика",
                "title": "Пользователь отклонил ваше приглашение",
                "greeting": f"Здравствуйте, {incoming_request.team.team_leader.get_greeting_name()}!",
                "main_text": main_text,
                "bottom_text": None,
                "button_text": None,
                "button_link": None
            }

            send_email.apply_async(kwargs={"email_data": email_data})

            return Response(status=204,
                            content=f"Запрос на вступление в команду {incoming_request.team.name} был отклонен")


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class TeamOutgoingRequestView(APIView):
    user = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')

        try:
            self.team = Team.objects.get(id=kwargs.get('team_pk'))
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if self.team.team_leader != self.user:
            return Response(status=400,
                            content="Вы не можете просматривать приглашения команды")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Просмотр всех исходящих запросов команды"""
        request_status = request.GET.get('request_status', None)
        outgoing_requests = self.team.team_requests.filter(request_type=TeamRequest.INCOMING)
        if request_status:
            outgoing_requests = outgoing_requests.filter(request_status=request_status)
        serializer = RequestSerializer(instance=outgoing_requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Создать командой запрос на приглашение пользователя в команду"""
        serializer = WriteTeamOutgoingRequestSerializer(data=request.data,
                                                        context={'user': self.user, 'team': self.team})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        main_text = f"""Команда '{data.team.name}' отправила вам приглашение на членство"""
        email_data = {
            "receivers": [data.user.email],
            "subject": "Уведомление на платформе Σ | Эврика",
            "title": "Вас пригласили в команду!",
            "greeting": f"Здравствуйте, {data.user.get_greeting_name()}!",
            "main_text": main_text,
            "bottom_text": None,
            "button_text": None,
            "button_link": None
        }

        send_email.apply_async(kwargs={"email_data": email_data})

        return Response(status=201, content={"id": str(data.id)})

    def delete(self, request, request_pk, *args, **kwargs):
        """Удалить приглашение на вступление в команду"""
        try:
            outgoing_request = TeamRequest.objects.get(id=request_pk,
                                                       team__team_leader=self.user,
                                                       request_type=TeamRequest.INCOMING,
                                                       request_status=TeamRequest.REQUEST_SUBMITTED)
        except ObjectDoesNotExist:
            return Response(status=404, content="Активный запрос не найден")
        outgoing_request.delete()
        return Response(status=204)


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class TeamIncomingRequestView(APIView):
    user = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.get('user')

        try:
            self.team = Team.objects.get(id=kwargs.get('team_pk'))
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        if self.team.team_leader != self.user:
            return Response(status=400,
                            content="Вы не можете просматривать запросы на вступление в команду")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Просмотр всех входящих запросов команды"""
        request_status = request.GET.get('request_status', None)
        incoming_requests = self.team.team_requests.filter(request_type=TeamRequest.OUTGOING)
        if request_status:
            incoming_requests = incoming_requests.filter(request_status=request_status)
        serializer = RequestSerializer(instance=incoming_requests, many=True)
        return Response(serializer.data)

    def put(self, request, request_pk, *args, **kwargs):
        """Принятие или отклонение запроса на вступление в команду"""
        try:
            incoming_request = TeamRequest.objects.get(id=request_pk,
                                                       request_type=TeamRequest.OUTGOING,
                                                       request_status=TeamRequest.REQUEST_SUBMITTED)
        except ObjectDoesNotExist:
            return Response(status=404, content="Запрос не найден")

        decision = request.data.get('decision', None)
        if decision is None:
            return Response(status=400, content="Не указано решение")
        if decision:
            incoming_request.request_status = TeamRequest.REQUEST_ACCEPTED
            incoming_request.save()
            incoming_request.team.members.add(incoming_request.user, through_defaults={'role': incoming_request.role,
                                                                                       'membership_requester': Membership.USER})

            main_text = f"""Ваш запрос о вступлении в команду '{incoming_request.team.name}' был одобрен. Поздравляем!"""
            email_data = {
                "receivers": [incoming_request.user.email],
                "subject": "Уведомление на платформе Σ | Эврика",
                "title": "Ваш запрос на вступление в команду был одобрен!",
                "greeting": f"Здравствуйте, {incoming_request.user.get_greeting_name()}!",
                "main_text": main_text,
                "bottom_text": None,
                "button_text": None,
                "button_link": None
            }

            send_email.apply_async(kwargs={"email_data": email_data})

            return Response(status=204, content=f"Вы приняли пользователя {incoming_request.user.snp} в команду")
        else:
            incoming_request.request_status = TeamRequest.REQUEST_DECLINED
            incoming_request.save()

            main_text = f"""Ваш запрос о вступлении в команду '{incoming_request.team.name}' был отклонен"""
            email_data = {
                "receivers": [incoming_request.user.email],
                "subject": "Уведомление на платформе Σ | Эврика",
                "title": "Ваш запрос на вступление в команду был отклонен.",
                "greeting": f"Здравствуйте, {incoming_request.user.get_greeting_name()}!",
                "main_text": main_text,
                "bottom_text": None,
                "button_text": None,
                "button_link": None
            }

            send_email.apply_async(kwargs={"email_data": email_data})
            return Response(status=204,
                            content=f"Вы отклонили запрос пользователя {incoming_request.user.snp} на вступление в команду")


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class TeamVacancyView(APIView):
    def get(self, request, *args, **kwargs):
        """Получить предложения по вступлению в команды"""
        user = kwargs.get('user')

        already_invited_teams = list(TeamRequest.objects.filter(user=user).values_list('team__id', flat=True))

        teams_looking_for_members = Team.objects.filter(is_looking_for_members=True).filter(
            ~Q(id__in=already_invited_teams))
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)

        suitable_teams = []
        less_suitable_teams = []

        for team in teams_looking_for_members:
            if does_team_need_this_user(team=team, user=user):
                suitable_teams.append(team)
            else:
                less_suitable_teams.append(team)

        suitable_teams = Team.objects.filter(id__in=[team.id for team in suitable_teams])
        less_suitable_teams = Team.objects.filter(id__in=[team.id for team in less_suitable_teams])

        if not suitable_teams:
            suitable_teams = less_suitable_teams

        return Response(team_vacancy_paginator(suitable_teams, less_suitable_teams, *get_params, current_user=user))


@method_decorator([tryexcept, auth, log_action], name='dispatch')
class UserVacancyView(APIView):
    def get(self, request, team_pk, *args, **kwargs):
        """Получить предложения по приглашению пользователей в команду"""
        try:
            team = Team.objects.get(id=team_pk)
        except ObjectDoesNotExist:
            return Response(status=404, content="Команда не найдена")

        #  Исключать пользователей, которые уже приглащены, либо которые состоят в команде

        users_already_invited_to_team = list(TeamRequest.objects.filter(team=team).values_list('user__id', flat=True))
        users_looking_for_team = User.objects.filter(profile__profile_settings__can_be_invited=True).filter(
            ~Q(teams__id=team_pk)).filter(~Q(id__in=users_already_invited_to_team))
        try:
            get_params = clean_get_params(request)
        except BadRequestException as error:
            return Response(status=400, content=error.message)

        suitable_users = []
        less_suitable_users = []

        # Неподходящие команды выводить, но в самом конце

        for user in users_looking_for_team:
            if does_team_need_this_user(team=team, user=user):
                suitable_users.append(user)
            else:
                less_suitable_users.append(user)
        suitable_users = User.objects.filter(id__in=[user.id for user in suitable_users])
        less_suitable_users = User.objects.filter(id__in=[user.id for user in less_suitable_users])
        if not suitable_users:
            suitable_users = less_suitable_users

        return Response(user_vacancy_extended_paginator(suitable_users, less_suitable_users, *get_params))
