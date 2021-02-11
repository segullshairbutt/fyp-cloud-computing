from django.urls import path

from devops.views import ProjectCreateView

urlpatterns = [
    path("project/create/", ProjectCreateView.as_view())
]