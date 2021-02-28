from django.urls import path

from devops.views import ProjectCreateView, ProjectListView, ProjectDetailView, ProjectMonitoringView, ProjectConfigView

urlpatterns = [
    path("projects/create/", ProjectCreateView.as_view()),
    path("projects/<int:pk>/start-monitoring/", ProjectMonitoringView.as_view()),
    path("projects/", ProjectListView.as_view()),
    path("projects/<int:pk>/", ProjectDetailView.as_view()),
    path("projects/<int:pk>/config/<str:config_key>/", ProjectConfigView.as_view()),
]
