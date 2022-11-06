import logging

from django.db.models import Count, Sum

from ideas.models import Idea, Post
from teams.models import Team, RequiredMembers, TeamRequest
from users.models import User, UserAddInfo

logger = logging.getLogger(__name__)


def minimax_normalization(current_value, min_value, max_value):
    """
    Минимаксная нормализация значения
    """

    if min_value == max_value:
        return 0
    return (current_value - min_value) / (max_value - min_value)


def missing_roles_in_team(team):
    """
    Возвращает список ролей, которые ищет команда
    """
    existing_team_members = team.members.all()
    missing_team_roles = []
    required_team_roles = RequiredMembers.objects.filter(team=team).values('role', 'role__name', 'amount')
    for required_team_role in required_team_roles:
        role_amount = required_team_role['amount']
        role_id = required_team_role['role']
        if role_amount <= 0:
            continue
        existing_role_team_members_count = existing_team_members.filter(membership__role=role_id).count()
        difference = role_amount - existing_role_team_members_count
        if difference > 0:
            missing_team_roles.append(role_id)
    return missing_team_roles


def does_team_need_this_user(team, user):
    user_roles = set(user.add_info.team_role.all().values_list('id', flat=True))
    missing_roles = set(missing_roles_in_team(team))
    return True if missing_roles & user_roles else False


def team_rating(team):
    """
    Возвращает активность команды
    """

    MAX_USERS = User.objects.count()
    MAX_TEAMS = Team.objects.count()
    MAX_IDEAS = Idea.objects.count()
    MAX_POSTS = Post.objects.count()
    BEST_RATING_SCORE = 2

    # Количество постов команды
    team_posts_count = team.idea.posts.count()

    if 0 <= team_posts_count <= 1:
        team_posts_count_rating = 5
    elif 1 < team_posts_count <= 4:
        team_posts_count_rating = 10
    elif 4 < team_posts_count <= 10:
        team_posts_count_rating = 15
    elif 10 < team_posts_count <= 20:
        team_posts_count_rating = 20
    else:
        team_posts_count_rating = 30

    normalized_team_posts_count_rating = minimax_normalization(team_posts_count_rating, 0, 30)
    # Количество комментариев в постах команды
    team_posts_comments_count = \
        team.idea.posts.annotate(comments_count=Count('comments')).aggregate(Sum('comments_count'))[
            'comments_count__sum']

    if not team_posts_comments_count:
        team_posts_comments_count = 0

    if 0 <= team_posts_comments_count <= 2:
        team_posts_comments_rating = 5
    elif 3 <= team_posts_comments_count <= 5:
        team_posts_comments_rating = 10
    elif 6 <= team_posts_comments_count <= 20:
        team_posts_comments_rating = 30
    else:
        team_posts_comments_rating = 50

    normalized_team_posts_comments_rating = minimax_normalization(team_posts_comments_rating, 5, 50)

    # Количество комментариев в идеи команды
    team_idea_comments_count = team.idea.comments.annotate(comments_count=Count('id')).aggregate(Sum('comments_count'))[
        'comments_count__sum']

    if not team_idea_comments_count:
        team_idea_comments_count = 0

    if 0 <= team_idea_comments_count <= 3:
        team_idea_comments_rating = 1
    elif 3 <= team_idea_comments_count <= 20:
        team_idea_comments_rating = 10
    elif 20 <= team_idea_comments_count <= 50:
        team_idea_comments_rating = 30
    else:
        team_idea_comments_rating = 50

    normalized_team_idea_comments_rating = minimax_normalization(team_idea_comments_rating, 1, 50)

    # Количество лайков идеи команды
    team_idea_likes_count = team.idea.likes.count()

    normalized_team_idea_likes_rating = minimax_normalization(team_idea_likes_count, 0, MAX_USERS)

    # Количество лайков постов команды
    team_posts_likes_count = team.idea.posts.annotate(likes_count=Count('likes')).aggregate(Sum('likes_count'))[
        'likes_count__sum']

    normalized_team_posts_likes_count = minimax_normalization(team_posts_likes_count, 0, MAX_USERS * team_posts_count)

    # Рейтинг идеи
    idea_rating = team.idea.rating

    normalized_idea_rating = minimax_normalization(idea_rating, 0, MAX_USERS * BEST_RATING_SCORE)

    # Количество участников команды
    team_members_count = team.members.count()

    if 0 <= team_members_count <= 1:
        team_members_count_rating = 10
    elif 2 <= team_members_count <= 3:
        team_members_count_rating = 25
    elif 4 <= team_members_count <= 5:
        team_members_count_rating = 35
    else:
        team_members_count_rating = 50

    normalized_team_members_count_rating = minimax_normalization(team_members_count_rating, 10, 50)

    # Количество входящих заявок на вступление в команду
    team_incoming_requests_count = team.team_requests.filter(request_type=TeamRequest.OUTGOING).count()

    normalized_team_incoming_requests_count = minimax_normalization(team_incoming_requests_count, 0, MAX_TEAMS)

    # Количество исходящих заявок на вступление в команду
    team_outgoing_requests_count = team.team_requests.filter(request_type=TeamRequest.INCOMING).count()

    normalized_team_outgoing_requests_count = minimax_normalization(team_outgoing_requests_count, 0, MAX_TEAMS)

    # Количество лайков идей участниками команды
    team_members_idea_likes_count = team.members.annotate(likes_count=Count('likes')).aggregate(Sum('likes_count'))[
        'likes_count__sum']

    normalized_team_members_idea_likes_count = minimax_normalization(team_members_idea_likes_count, 0,
                                                                     MAX_IDEAS * team_members_count)

    # Количество лайков постов участниками команды
    team_members_post_likes_count = \
        team.members.annotate(likes_count=Count('post_likes')).aggregate(Sum('likes_count'))[
            'likes_count__sum']

    normalized_team_members_post_likes_count = minimax_normalization(team_members_post_likes_count, 0,
                                                                     MAX_POSTS * team_members_count)

    # Насколько интересуются командой
    rate_1 = (0.03 * normalized_team_posts_comments_rating +
              0.03 * normalized_team_idea_comments_rating +
              0.06 * normalized_team_idea_likes_rating +
              0.05 * normalized_team_posts_likes_count +
              0.12 * normalized_team_incoming_requests_count)

    # Активность участников команды
    rate_2 = (0.04 * normalized_team_members_idea_likes_count +
              0.04 * normalized_team_members_post_likes_count)

    #  Что команда из себя представляет
    rate_3 = (0.2 * normalized_idea_rating -
              0.3 * normalized_team_members_count_rating +
              0.08 * normalized_team_outgoing_requests_count +
              0.05 * normalized_team_posts_count_rating)

    total_team_rate = (rate_1 + rate_2 + rate_3)

    return total_team_rate


def user_rating(user):
    # Рейтинг университета, который закончил пользователь
    BEST_UNIVERSITY_RATING_SCORE = 100
    MAX_USERS = User.objects.count()

    if user.add_info.education_university:
        user_university_rating = user.add_info.education_university.rating
    else:
        user_university_rating = 0

    normalized_user_university_rating = minimax_normalization(user_university_rating, 0, BEST_UNIVERSITY_RATING_SCORE)

    # Рейтинг образования пользователя
    if user.add_info.education_level == UserAddInfo.BASIC_GENERAL_EDUCATION:
        user_education_level_rating = 0
    elif user.add_info.education_level == UserAddInfo.SECONDARY_SCHOOL:
        user_education_level_rating = 5
    elif user.add_info.education_level == UserAddInfo.LOWER_POST_SECONDARY_VOCATIONAL_EDUCATION:
        user_education_level_rating = 10
    elif user.add_info.education_level == UserAddInfo.INCOMPLETE_HIGHER_EDUCATION:
        user_education_level_rating = 20
    elif user.add_info.education_level == UserAddInfo.BACHELOR:
        user_education_level_rating = 40
    elif user.add_info.education_level == UserAddInfo.SPECIALIST:
        user_education_level_rating = 50
    elif user.add_info.education_level == UserAddInfo.MASTER:
        user_education_level_rating = 50
    elif user.add_info.education_level == UserAddInfo.POSTGRADUATE:
        user_education_level_rating = 70
    elif user.add_info.education_level == UserAddInfo.PHD:
        user_education_level_rating = 100
    else:
        user_education_level_rating = 0

    normalized_user_education_level_rating = minimax_normalization(user_education_level_rating, 0, 100)

    # Рейтинг научной деятельности
    user_iar_rating = 100 if user.add_info.has_iar else 0
    normalized_user_iar_rating = minimax_normalization(user_iar_rating, 0, 100)
    # Рейтинг бизнес деятельности
    user_has_own_company_rating = 100 if user.add_info.has_own_company else 0
    normalized_user_has_own_company_rating = minimax_normalization(user_has_own_company_rating, 0, 100)

    # Рейтинг профессионального опыта
    if user.add_info.work_experience:
        user_work_experience_rating = 15 * user.add_info.work_experience
    else:
        user_work_experience_rating = 10

    normalized_user_work_experience_rating = minimax_normalization(user_work_experience_rating, 0, 15 * 60)

    #  Рейтинг опыта участия в хакатонах
    if user.add_info.hack_experience:
        user_hack_experience_rating = 13 * user.add_info.hack_experience
    else:
        user_hack_experience_rating = 10

    normalized_user_hack_experience_rating = minimax_normalization(user_hack_experience_rating, 0, 13 * 60)

    # Рейтинг занятости
    if user.add_info.employment == UserAddInfo.FULL:
        user_employment_status_rating = 80
    elif user.add_info.employment == UserAddInfo.PART:
        user_employment_status_rating = 60
    elif user.add_info.employment == UserAddInfo.PROJECT:
        user_employment_status_rating = 40
    elif user.add_info.employment == UserAddInfo.VOLUNTEER:
        user_employment_status_rating = 30
    elif user.add_info.employment == UserAddInfo.TRAINEE:
        user_employment_status_rating = 35
    elif user.add_info.employment == UserAddInfo.BUSINESS:
        user_employment_status_rating = 100
    elif user.add_info.employment == UserAddInfo.SELF_EMPLOYED:
        user_employment_status_rating = 55
    elif user.add_info.employment == UserAddInfo.UNEMPLOYED:
        user_employment_status_rating = 0
    else:
        user_employment_status_rating = 15

    normalized_user_employment_status_rating = minimax_normalization(user_employment_status_rating, 0, 100)

    # Количество команд, в которых состоит пользователь
    user_teams_count = user.teams.count()
    if 0 <= user_teams_count <= 1:
        user_teams_count_rating = 100
    elif 2 <= user_teams_count <= 3:
        user_teams_count_rating = 30
    elif 4 <= user_teams_count <= 5:
        user_teams_count_rating = 10
    else:
        user_teams_count_rating = 0

    normalized_user_teams_count_rating = minimax_normalization(user_teams_count_rating, 0, 100)

    # Количество приглашений на вступление в команду
    user_incoming_requests_count = user.user_requests.filter(request_type=TeamRequest.INCOMING).count()

    normalized_user_incoming_requests_count_rating = minimax_normalization(user_incoming_requests_count, 0, MAX_USERS)

    # Количество запросов на вступление в команду
    user_outgoing_requests_count = user.user_requests.filter(request_type=TeamRequest.OUTGOING).count()

    normalized_user_outgoing_requests_count_rating = minimax_normalization(user_outgoing_requests_count, 0, MAX_USERS)

    # Рейтинг пользователя
    total_user_rate = (
            0.15 * normalized_user_university_rating +
            0.1 * normalized_user_education_level_rating +
            0.05 * normalized_user_iar_rating +
            0.05 * normalized_user_has_own_company_rating +
            0.2 * normalized_user_work_experience_rating +
            0.8 * normalized_user_hack_experience_rating -
            0.04 * normalized_user_employment_status_rating -
            0.1 * normalized_user_teams_count_rating +
            0.13 * normalized_user_incoming_requests_count_rating +
            0.1 * normalized_user_outgoing_requests_count_rating)

    return total_user_rate
