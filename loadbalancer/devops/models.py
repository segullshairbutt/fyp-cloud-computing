from jsonfield import JSONField
from django.db import models
from django.contrib.auth.models import User


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


class Path(models.Model):
    name = models.CharField(max_length=50)


class Method(models.Model):
    name = models.CharField(max_length=10)
    extra_fields = JSONField()

    path = models.ForeignKey(Path, on_delete=models.CASCADE)


class Endpoint(models.Model):
    kubernetes = models.ForeignKey(Kubernetes, on_delete=models.CASCADE)
    port = models.PositiveIntegerField(primary_key=True)
    path = models.OneToOneField(Path, on_delete=models.CASCADE, related_name="endpoint_path")
