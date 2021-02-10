import os

from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User

from constants import ProjectPaths


class Project(models.Model):
    name = models.CharField(max_length=100)
    directory = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    @property
    def helm_chart_name(self):
        return f"open-api-app-{self.username}-{self.name.replace('_', '-')}"

    @property
    def config_data_path(self):
        return os.path.join(self.directory, "config_data")

    @property
    def dockerfile_path(self):
        return os.path.join(self.directory, "DOCKERFILE")

    @property
    def helm_chart_path(self):
        return os.path.join(self.directory, ProjectPaths.HELM_CHARTS)

    @property
    def helm_chart_templates_path(self):
        return os.path.join(self.directory, ProjectPaths.HELM_CHARTS, ProjectPaths.TEMPLATES)

    @property
    def helm_deployment_path(self):
        return os.path.join(self.directory, ProjectPaths.HELM_DEPLOYMENTS)


class Path(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="path_urls", null=True)


class Method(models.Model):
    name = models.CharField(max_length=10)
    extra_fields = JSONField()

    path = models.ForeignKey(Path, on_delete=models.CASCADE)
