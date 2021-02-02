import os

from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User

from constants import ProjectPaths


class Github(models.Model):
    url = models.URLField(primary_key=True, blank=False, null=False)
    cloned_directory = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.url


class Docker(models.Model):
    github = models.OneToOneField(Github, on_delete=models.CASCADE, related_name="docker_profile")
    docker_image = models.CharField(max_length=200, blank=False, null=False)
    default_docker_filepath = models.CharField(max_length=200, blank=False, null=False)
    deployment_path = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.docker_image


class Kubernetes(models.Model):
    docker = models.OneToOneField(Docker, on_delete=models.CASCADE, related_name="kubernetes_profile")
    deployment_name = models.CharField(max_length=100, blank=False, null=False)
    config_data_path = models.CharField(max_length=200, blank=False, null=False)
    yaml_deployments = models.CharField(max_length=200, blank=False, null=False)
    def_helmchart_path = models.CharField(max_length=200, null=False, blank=False)
    helm_deployments = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.deployment_name


class Endpoints(models.Model):
    kubernetes = models.ForeignKey(Kubernetes, on_delete=models.CASCADE)
    ports = models.PositiveIntegerField(primary_key=True)

    def __str__(self):
        return str(self.ports)


# the actual model that has been used yet starts from here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    docker_image_name = models.CharField(max_length=200)
    kubernetes_deployment_name = models.CharField(max_length=200)
    directory = models.CharField(max_length=500)

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
# and ends here

class Endpoint(models.Model):
    kubernetes = models.ForeignKey(Kubernetes, on_delete=models.CASCADE)
    port = models.PositiveIntegerField(primary_key=True)
    path = models.OneToOneField(Path, on_delete=models.CASCADE, related_name="endpoint_path")

