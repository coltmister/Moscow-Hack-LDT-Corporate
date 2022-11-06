from django.urls import path

from iam import account, impersonation, sessions, login

urlpatterns = [

    path('update_password_via_email/', account.UpdatePasswordViaEmailView.as_view()),

    path('users/sessions/', sessions.UserSessionsView.as_view()),
    path('users/<uuid:user_uuid>/sessions/', sessions.UserSessionsView.as_view()),
    path('users/<uuid:user_uuid>/sessions/<uuid:session_id>/', sessions.UserSessionsView.as_view()),
    path('users/<uuid:user_uuid>/logout-user/', sessions.LogoutUserView.as_view()),
    path('users/logout-user/', sessions.LogoutUserView.as_view()),
    path('users/devices/', sessions.MySessionDevicesView.as_view()),
    path('users/<uuid:user_uuid>/activity-status/', account.ChangeUserActivityStatusView.as_view()),

    path('impersonation/<uuid:user_uuid>/', impersonation.ImpersonateUserView.as_view()),
    path('impersonation/redirect/', impersonation.ImpersonateUserLinkView.as_view()),

    path('auth/obtain-tokens/', login.ObtainTokensView.as_view()),
    path('auth/refresh-token/', login.RefreshTokenView.as_view()),
    path('auth/logout/', login.logout),
    path('auth/login/', login.login),
    path('auth/login-page/', login.login_page),
]
