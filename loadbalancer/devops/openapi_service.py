import json
import os
import logging
from random import choice

from devops.constants import METHOD_TEMPLATE, GET_METHOD_TEMPLATE
from devops.models import Project, Path, Method
from monitoring_app.data_monitorer import data_monitor

USERNAME = 'admin'
VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def create_project(project_name):
    VERBOSE_LOGGER.info("creating project...")
    project_directory = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], USERNAME, project_name)
    if os.path.isdir(project_directory):
        raise IsADirectoryError("Project with this name already exists.")
    else:
        os.makedirs(project_directory)
        LOGGER.info("project directory created..")

    project = Project()
    project.name = project_name
    project.directory = project_directory
    project.docker_image_name = 'segullshairbutt/website:' + project_name
    project.kubernetes_deployment_name = 'deployement_' + project_name

    os.mkdir(project.docker_deployment_path)
    os.mkdir(project.config_data_path)
    os.mkdir(project.yaml_deployment_path)
    os.mkdir(project.helm_deployment_path)
    os.makedirs(project.helm_chart_templates_path)

    LOGGER.info("project directories created..")
    return project.save()


def create_endpoint_path(project_id, path_name, number_of_methods):
    complete_path_name = '/' + path_name if path_name[0] != '/' else path_name
    path = Path(name=complete_path_name)
    path.project_id = project_id
    path.save()
    for a in range(number_of_methods):
        name = choice(["post", "delete", "put", "get", "patch"])
        if name == "get":
            method_template = GET_METHOD_TEMPLATE
        else:
            method_template = METHOD_TEMPLATE
        method = Method(path=path, name=name, extra_fields=json.dumps(method_template))
        method.save()


