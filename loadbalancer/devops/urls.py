from django.urls import path

from devops.views import ProjectCreateView, ProjectListView, ProjectDetailView, ProjectMonitoringView

urlpatterns = [
    path("project/create/", ProjectCreateView.as_view()),
    path("project/<int:pk>/start-monitoring/", ProjectMonitoringView.as_view()),
    path("projects/", ProjectListView.as_view()),
    path("projects/<int:pk>/", ProjectDetailView.as_view()),
]
