import subprocess
import os
import logging
from random import choice

from devops import constants
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
    project.username = USERNAME
    project.directory = project_directory

    os.mkdir(project.config_data_path)
    os.mkdir(project.helm_deployment_path)
    os.makedirs(project.helm_chart_templates_path)

    with(open(os.path.join(project.helm_chart_path, "Chart.yaml"), "w")) as chart_file:
        LOGGER.info("writing Chart.YAML file")
        chart_file.write(f"""apiVersion: v2 #mandatory
    name: open-api-chart #mandatory
    description: A Helm chart for Kubernetes
    type: application
    version: 0.1.0 #mandatory
    appVersion: 1.0""")
    # installing the helm for first time
    subprocess.call(["helm", "install", project.helm_chart_name, project.helm_chart_path])

    LOGGER.info("project directories created..")
    return project.save()


def create_endpoint_path(project_id, path_name, number_of_methods, schema_name):
    complete_path_name = '/' + path_name if path_name[0] != '/' else path_name
    path = Path(name=complete_path_name)
    path.project_id = project_id
    path.save()
    for a in range(number_of_methods):
        name = choice(["post", "delete", "put", "get", "patch"])
        if name == "get":
            method_template = constants.GET_METHOD_TEMPLATE
        else:
            method_template = constants.generate_method(schema_name)
        method = Method(path=path, name=name, extra_fields=method_template)
        method.save()


def start_monitoring(project_id):
    project = Project.objects.get(id=project_id)

    data_monitor(project)

