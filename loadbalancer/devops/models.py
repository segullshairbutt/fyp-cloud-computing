from django.db import models
from django.contrib.auth.models import User


class Github(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(primary_key=True, blank=False, null=False)
    cloned_directory = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.url


class Docker(models.Model):
    github = models.OneToOneField(Github, on_delete=models.CASCADE)
    docker_image = models.CharField(max_length=200, blank=False, null=False)
    default_docker_filepath = models.CharField(max_length=200, blank=False, null=False)
    deployment_path = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.docker_image


class Kubernetes(models.Model):
    docker = models.OneToOneField(Docker, on_delete=models.CASCADE)
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
