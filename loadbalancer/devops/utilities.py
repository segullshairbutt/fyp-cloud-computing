import os
import subprocess
import logging.config

from git import Repo

from .files_formatter import (
    get_values_file_format, get_charts_file_format,
    get_deployment_file_format, get_service_file_format)

# getting logger object defined in setting.py
LOGGER = logging.getLogger("root")


def clone_repo(url, cloning_directory):
    try:
        LOGGER.info("started cloning directory.")
        cloned_repo = Repo.clone_from(url, cloning_directory)
        cloned_repo.close()
        LOGGER.debug("repo cloned.")
        return True

    except Exception as e:
        LOGGER.error("Error on cloning", e)
        return False


def create_image(docker):
    """Creating an image from given working directory which contains a dockerfile."""
    LOGGER.info(msg="started creating image.")
    subprocess.call(
        ['docker', 'build', '-t', f"{docker.docker_image}:fyp_kubernetes", '.'],
        cwd=docker.github.cloned_directory)
    LOGGER.debug(msg="finished creating image.")


def push_image(docker):
    """Pushing the image to Dockerhub dockerfile."""
    LOGGER.info(msg="pushing the image.")
    subprocess.call(['docker', 'push', f"{docker.docker_image}:fyp_kubernetes"])
    LOGGER.info(msg="finished pushing the image.")


def create_chart(kuburnetes, services_ports):
    LOGGER.info("creating chart.")
    docker_image = str(kuburnetes.docker.docker_image)
    DOCKERFILE_PATH = kuburnetes.docker.default_docker_filepath
    EXPOSE_PORT = 3000  # default port
    # open docker file to get expose port
    with open(DOCKERFILE_PATH, "r") as dockerfile:
        for content in dockerfile:
            if "EXPOSE" in content:
                EXPOSE_PORT = content.split()
    # writing values.yaml file
    with open(os.path.join(kuburnetes.def_helmchart_path, 'values.yaml'), "w") as file:
        file.write(get_values_file_format(
            docker_image, EXPOSE_PORT[1], kuburnetes.deployment_name))

    # writing chart.yaml file
    with open(os.path.join(kuburnetes.def_helmchart_path, 'Chart.yaml'), "w") as file:
        file.write(get_charts_file_format(kuburnetes.deployment_name))

    template_dir = os.path.join(kuburnetes.def_helmchart_path, 'templates')
    services_path = os.path.join(template_dir, 'service.yaml')
    deployment_path = os.path.join(template_dir, 'deployment.yaml')

    # writing deployment.yaml file
    with open(deployment_path, "w") as file:
        file.write(get_deployment_file_format(kuburnetes.deployment_name))
    # writing service.yaml file
    with open(services_path, 'w')as file:
        file.write(get_service_file_format(services_ports))
    LOGGER.info("finished creating chart.")


def deploy_chart(kuburnetes):
    LOGGER.info("deploying chart.")
    clone_dir = os.path.dirname(kuburnetes.docker.default_docker_filepath)
    helm_chart_name = os.path.basename(kuburnetes.def_helmchart_path)
    LOGGER.debug("Helm Chart name.", helm_chart_name)
    subprocess.call(
        ['helm', 'install', kuburnetes.deployment_name, helm_chart_name], cwd=clone_dir)
    LOGGER.debug("finished deploying the chart.")


def get_config_data_file(kuburnetes, file_type, filename):
    LOGGER.info("getting config data file.")
    helm_template_dir = os.path.join(kuburnetes.def_helmchart_path, 'templates')
    if file_type == "defDocker":
        filepath = kuburnetes.docker.default_docker_filepath
    if filename == "service.yaml":
        filepath = os.path.join(helm_template_dir, filename)
    if filename == "deployment.yaml":
        filepath = os.path.join(helm_template_dir, filename)
    if filename == "values.yaml":
        filepath = os.path.join(kuburnetes.def_helmchart_path, filename)
    if filename == "Chart.yaml":
        filepath = os.path.join(kuburnetes.def_helmchart_path, filename)

    if file_type == "newConfig":
        filepath = os.path.join(kuburnetes.config_data_path, filename)
    if file_type == "newyaml":
        filepath = os.path.join(kuburnetes.yaml_deployments, filename)
    if file_type == "newDocker":
        filepath = os.path.join(kuburnetes.docker.deployment_path, filename)

    file_content = []
    with open(filepath, "r") as file:
        for data in file:
            file_content.append(data)
    LOGGER.debug("finished getting config data file.")
    return file_content
