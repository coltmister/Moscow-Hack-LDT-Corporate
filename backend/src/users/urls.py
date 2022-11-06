from django.urls import path

from users import views, constants

urlpatterns = [
    path('', views.UserView.as_view()),
    path('<uuid:user_pk>', views.UserView.as_view()),
    path('add-info', views.UserAddInfoView.as_view()),
    path('<uuid:user_pk>/add-info', views.UserAddInfoView.as_view()),
    path('me', views.UserMeView.as_view()),
    path('skills', constants.SkillsView.as_view()),
    path('interests', constants.InterestsView.as_view()),
    path('country', constants.CountryView.as_view()),
    path('university', constants.UniversityView.as_view()),
    path('team-roles', constants.TeamRoleView.as_view()),
    path('ideas', views.UserIdeasView.as_view()),

    path('<str:username_pk>', views.UserView.as_view()),
    path('<uuid:user_pk>/verify', views.VerifyUser.as_view()),
    path('<uuid:user_pk>/ideas', views.UserIdeasView.as_view()),
    path('<uuid:user_pk>/admin', views.PromoteUserToAdmin.as_view()),
    path('me/profile', views.UserProfileView.as_view()),  # Информация о своем профиле
    path('me/profile-settings', views.UserProfileSettingsView.as_view()),  # Публичность профиля
    path('me/avatar', views.UserAvatarView.as_view()),  # Фото профиля
    path('<uuid:user_pk>/profile', views.UserProfileView.as_view()),
    path('<uuid:user_pk>/teams', views.UserTeamsListView.as_view()),
    path('me/teams', views.UserTeamsListView.as_view()),

]
