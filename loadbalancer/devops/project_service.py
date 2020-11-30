import json
import os
import logging
import subprocess
# import tempfile
import zipfile
from copy import deepcopy
from random import choice

from .constants import METHOD_TEMPLATE
from .models import Github, Docker, Kubernetes, Endpoints, Endpoint, Method, Path
from .utilities import clone_repo, create_image, push_image, create_chart, deploy_chart
from monitoring_app.data_monitorer import data_monitor

LOGGER = logging.getLogger("root")


def clone_github_repo(clone_url, dir_name):
    try:
        git_repo = Github.objects.filter(url=clone_url)
        if not git_repo:
            cloning_dir = os.path.join(os.getcwd(), str(dir_name))

            github = Github(url=clone_url, cloned_directory=cloning_dir)

            # cloning the repo in given directory
            if clone_repo(clone_url, cloning_dir):
                github.save()
            else:
                LOGGER.error("Error: can't download the specified repo")
                raise AssertionError("Download failed.")
        else:
            LOGGER.error("Error: Repo already exists.")
    except Exception as e:
        LOGGER.error({"error": e})


def delete_project(url):
    LOGGER.info("delete project")
    github = Github.objects.filter(url=url).first()

    if not github:
        raise AssertionError("no github projects found.")

    docker = Docker.objects.filter(github=github).first()

    if not docker:
        LOGGER.warning("project isn't deployed.")
    else:
        docker_image = docker.docker_image
        LOGGER.info("Deleting docker image")
        subprocess.call(['docker', 'rmi', docker_image])

        kubernetes = Kubernetes.objects.filter(docker=docker).first()
        deployment_name = kubernetes.deployment_name
        LOGGER.info("uninstalling helm chart")
        subprocess.call(['helm', 'uninstall', str(deployment_name)])

    github.delete()
    LOGGER.info("delete project finished.")


def deploy_project(project_url, dir_name, api_name):
    github = Github.objects.filter(url=project_url).first()

    if not github:
        raise AssertionError("No projects found with this url.")

    docker = Docker.objects.filter(github=github).first()
    # docker = Docker.objects.filter(github=github[0])

    if docker:
        raise AssertionError("url already deployed.")

    try:
        cloned_dir = github.cloned_directory
        # image_name = str('segullshairbutt/' + str(request.user) + str(os.path.basename(cloned_dir)))
        # here we are going to provide the path for pushing
        image_name = 'segullshairbutt/website'
        deployment_path = os.path.join(cloned_dir, "docker_deployments")
        os.mkdir(deployment_path)

        # this path is already available
        default_docker_file_path = os.path.join(cloned_dir, "Dockerfile")
        docker = Docker(
            github=github, docker_image=image_name, deployment_path=deployment_path,
            default_docker_filepath=default_docker_file_path)
        create_image(docker)
        # push_image(docker)

        config_data_path = os.path.join(cloned_dir, "config_data")
        os.mkdir(config_data_path)

        yaml_deployments_path = os.path.join(cloned_dir, "yaml_deployments")
        os.mkdir(yaml_deployments_path)

        helm_chart_path = os.path.join(cloned_dir, "def_helmchart")
        templates = os.path.join(helm_chart_path, "templates")
        os.makedirs(templates)

        helm_deployments = os.path.join(cloned_dir, 'helm_deployments')
        os.mkdir(helm_deployments)

        services_ports = []
        port_low_range = 4000
        port_up_range = 4005

        # prev_docker_obj = Docker.objects.filter(github=github[0])
        # # if length >0 it means there is already project exists with deployment
        # if prev_docker_obj:
        #     deploymentTag = len(prev_docker_obj) + 1

        endpoints = Endpoints.objects.all()
        # will get a port that's is not occupied by any other endpoint
        if endpoints:
            port_low_range = endpoints[len(endpoints) - 1].ports + 1
            port_up_range = port_low_range + 5

        for ports in range(port_low_range, port_up_range):
            services_ports.append(ports)

        deploymentName = str(dir_name) + "-nodeapp-" + str(len(Docker.objects.all()) + 1)

        kubernetes = Kubernetes(docker=docker,
                                config_data_path=config_data_path, yaml_deployments=yaml_deployments_path,
                                deployment_name=deploymentName, def_helmchart_path=helm_chart_path,
                                helm_deployments=helm_deployments)

        create_chart(kuburnetes=kubernetes, services_ports=services_ports)

        # deploy_chart(kuburnetes=kubernetes)

        docker.save()
        kubernetes.save()

        # save ports to endpoints
        for port in services_ports:
            # endpoints = Endpoints(kubernetes=kubernetes, ports=port)
            # endpoints.save()

            name = choice(["POST", "DELETE", "PUT", "GET", "PATCH"])
            path = Path(name=api_name)
            path.save()

            method = Method(path=path, name=name, extra_fields=json.dumps(METHOD_TEMPLATE))
            method.save()

            endpoint = Endpoint(kubernetes=kubernetes, port=port, path=path)
            endpoint.save()

    except Exception as e:
        raise e


def zip_dir():
    LOGGER.info("Zipping directory.")
    zip_file = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk("temp/"):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()
    LOGGER.info("Zipping directory finished.")


class Filepaths:
    def __init__(self):
        self.default_docker_filepath = None
        self.docker_deployment_path = None
        self.docker_image = None
        self.config_data_path = None
        self.yaml_filepath = None
        self.helm_deployment_path = None


def start_monitoring(github):
    docker = Docker.objects.get(github=github)
    kubernetes = Kubernetes.objects.get(docker=docker)

    # service_ports = kubernetes.endpoints_set.all()
    end_points = kubernetes.endpoint_set.all()

    paths = Filepaths()
    paths.default_docker_filepath = docker.default_docker_filepath
    paths.docker_deployment_path = docker.deployment_path
    paths.docker_image = docker.docker_image
    paths.config_data_path = kubernetes.config_data_path
    paths.yaml_filepath = kubernetes.yaml_deployments
    paths.helm_deployment_path = kubernetes.helm_deployments

    data_monitor(paths, end_points)
    # main.run(docker, kubernetes, service_ports)
