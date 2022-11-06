from django.urls import path

from teams import views

urlpatterns = [
    path('', views.TeamView.as_view()),
    path('<uuid:team_pk>', views.TeamView.as_view()),
    path('<uuid:team_pk>/add-members', views.AddUserToTeamView.as_view()),
    path('<uuid:team_pk>/users/<uuid:user_pk>/kick', views.KickUserFromTeamView.as_view()),
    path('<uuid:team_pk>/leave', views.LeaveTeamView.as_view()),
    path('<uuid:team_pk>/users/<uuid:user_pk>/set-role', views.SetUserTeamRole.as_view()),

    path('outgoing-request', views.UserOutgoingRequestView.as_view()),
    path('outgoing-request/<uuid:request_pk>', views.UserOutgoingRequestView.as_view()),

    path('incoming-request', views.UserIncomingRequestView.as_view()),
    path('incoming-request/<uuid:request_pk>', views.UserIncomingRequestView.as_view()),

    path('<uuid:team_pk>/outgoing-request', views.TeamOutgoingRequestView.as_view()),
    path('<uuid:team_pk>/outgoing-request/<uuid:request_pk>', views.TeamOutgoingRequestView.as_view()),

    path('<uuid:team_pk>/incoming-request', views.TeamIncomingRequestView.as_view()),
    path('<uuid:team_pk>/incoming-request/<uuid:request_pk>', views.TeamIncomingRequestView.as_view()),

    path('team-vacancy', views.TeamVacancyView.as_view()),
    path('<uuid:team_pk>/user-vacancy', views.UserVacancyView.as_view()),

]
