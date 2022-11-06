from django.urls import path

from ideas.feed.views import FeedIdeaView
from ideas.posts.views import PostView, PostLikesView, PostCommentsView, PostFileUploadView
from ideas.views import IdeaView, IdeaCommentsView, IdeaInformationView, IdeaSettingsView, \
    IdeaStatusView, IdeaFileUploadView, IdeaLikesView, IdeaCategoryView

urlpatterns = [
    path('', IdeaView.as_view()),  # +
    path('files/', IdeaFileUploadView.as_view()),  # +
    path('<uuid:idea_id>/', IdeaView.as_view()),  # +
    path('<uuid:idea_id>/settings/', IdeaSettingsView.as_view()),  # +

    path('<uuid:idea_id>/comments/', IdeaCommentsView.as_view()),  # +
    path('<uuid:idea_id>/comments/<uuid:comment_id>/', IdeaCommentsView.as_view()),  # +

    path('<uuid:idea_id>/information/', IdeaInformationView.as_view()),  # +

    path('<uuid:idea_id>/files/', IdeaFileUploadView.as_view()),  # +
    path('<uuid:idea_id>/files/<uuid:file_id>', IdeaFileUploadView.as_view()),  # +

    path('<uuid:idea_id>/status/', IdeaStatusView.as_view()),  # +
    path('<uuid:idea_id>/category/', IdeaCategoryView.as_view()),  # +
    path('<uuid:idea_id>/likes/', IdeaLikesView.as_view()),  # +

    path('posts/', PostView.as_view()),
    path('<uuid:idea_id>/posts/', PostView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/', PostView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/files/', PostFileUploadView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/files/<uuid:file_id>', PostFileUploadView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/likes/', PostLikesView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/comments/', PostCommentsView.as_view()),
    path('<uuid:idea_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>', PostCommentsView.as_view()),

    path('status/', IdeaStatusView.as_view()),  # +
    path('category/', IdeaCategoryView.as_view()),  # +
    path('feed/', FeedIdeaView.as_view()),  # +
]
