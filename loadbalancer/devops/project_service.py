import os
import logging
import subprocess
# import tempfile
import zipfile

from .models import Github, Docker, Kubernetes, Endpoints
from .utilities import clone_repo, create_image, push_image, create_chart, deploy_chart

logger = logging.getLogger(__name__)


def clone_github_repo(clone_url, logged_in_user):
    try:
        git_repo = Github.objects.filter(user=logged_in_user, url=clone_url)
        if not git_repo:
            DIR = os.getcwd()
            DIR = os.path.join(DIR, str(logged_in_user))
            cloning_dir = DIR
            # cloning_dir = tempfile.mkdtemp(dir=DIR)

            github = Github(user=logged_in_user, url=clone_url, cloned_directory=cloning_dir)

            # cloning the repo in given directory
            if clone_repo(clone_url, cloning_dir):
                github.save()
            else:
                logger.error("Error: can't download the specified repo")
                raise AssertionError("Download failed.")
        else:
            logger.error("Error: Repo already exists.")
    except Exception as e:
        logger.error({"error": e})


def delete_project(url, user):
    logger.info("delete project")
    github_project = Github.objects.filter(user=user, url=url)

    if not github_project:
        raise AssertionError("no github projects found.")

    docker = Docker.objects.filter(github=github_project[0])

    if not docker:
        logger.warning("project isn't deployed.")
    else:
        docker_image = docker[0].docker_image
        logger.info("Deleting docker image")
        subprocess.call(['docker', 'rmi', docker_image])

        kubernetes = Kubernetes.objects.filter(docker=docker[0])
        deployment_name = kubernetes[0].deployment_name
        logger.info("uninstalling helm chart")
        subprocess.call(['helm', 'uninstall', str(deployment_name)])

    github_project.delete()
    logger.info("delete project finished.")


def deploy_project(project_url, logged_in_user):
    github = Github.objects.filter(user=logged_in_user, url=project_url)

    if not github:
        raise AssertionError("No projects found with this url.")

    docker = Docker.objects.filter(github=github[0])

    if docker:
        raise AssertionError("url already deployed.")

    try:
        cloned_dir = github[0].cloned_directory
        # image_name = str('segullshairbutt/' + str(request.user) + str(os.path.basename(cloned_dir)))
        # here we are going to provide the path for pushing
        image_name = 'segullshairbutt/website'
        deployment_path = os.path.join(cloned_dir, "docker_deployments")
        os.mkdir(deployment_path)

        # this path is already available
        default_docker_file_path = os.path.join(cloned_dir, "Dockerfile")
        docker = Docker(
            github=github[0], docker_image=image_name, deployment_path=deployment_path,
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
        if endpoints:
            port_low_range = endpoints[len(endpoints) - 1].ports + 1
            port_up_range = port_low_range + 5

        for ports in range(port_low_range, port_up_range):
            services_ports.append(ports)

        deploymentName = str(logged_in_user) + "-nodeapp-" + str(len(Docker.objects.all()) + 1)

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
            endpoints = Endpoints(kubernetes=kubernetes, ports=port)
            endpoints.save()

    except Exception as e:
        raise e


def zip_dir(path):
    zip_file = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()
