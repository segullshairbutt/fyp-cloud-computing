from django.urls import path

from devops.views import (
    ProjectCreateView, ProjectListView, ProjectDetailView, ProjectMonitoringView,
    ProjectConfigView, get_deployments_download_link)

urlpatterns = [
    path("projects/create/", ProjectCreateView.as_view()),
    path("projects/<int:pk>/start-monitoring/", ProjectMonitoringView.as_view()),
    path("projects/", ProjectListView.as_view()),
    path("projects/<int:pk>/", ProjectDetailView.as_view()),
    path("projects/<int:project_id>/download", get_deployments_download_link),
    path("projects/<int:pk>/config/<str:config_key>/", ProjectConfigView.as_view()),
]
