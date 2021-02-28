import json
import shutil
import subprocess
import os
import logging
from random import choice

from constants import X_CLUSTERS, PATHS, INFO, X_LOCATION, X_STORAGE_LEVEL, COMPONENTS, SCHEMAS, X_METRICS
from deployment_generator.models import Image
from devops import constants
from devops.constants import CLUSTER_TEMPLATE
from devops.models import Project, Path, Method
from monitoring_app.constants import NEW_CONFIG
from monitoring_app.data_monitorer import data_monitor

USERNAME = 'admin'
VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def create_project(project_name, initial_config, worker_nodes):
    VERBOSE_LOGGER.info("creating project...")
    project_name = project_name.lower()
    project_directory = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], USERNAME, project_name)
    if os.path.isdir(project_directory):
        raise IsADirectoryError("Project with this name already exists.")
    else:
        os.makedirs(project_directory)
        LOGGER.info("project directory created..")

    initial_config[INFO][X_CLUSTERS] = CLUSTER_TEMPLATE
    for path_name, path in initial_config[PATHS].items():
        for method_name, method in path.items():
            method[X_METRICS] = {"load": ""}
            method[X_LOCATION] = {"$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c1"}

    for schema_name, schema in initial_config[COMPONENTS][SCHEMAS].items():
        schema[X_STORAGE_LEVEL] = "pod"

    project = Project()
    project.initial_config = initial_config
    project.worker_nodes = worker_nodes
    project.name = project_name
    project.username = USERNAME
    project.directory = project_directory

    os.mkdir(project.config_data_path)
    os.mkdir(project.helm_deployment_path)
    os.makedirs(project.helm_chart_templates_path)

    with(open(os.path.join(project.helm_chart_path, "Chart.yaml"), "w")) as chart_file:
        LOGGER.info("writing Chart.YAML file")
        chart_file.write(f"""apiVersion: v2 #mandatory
name: {project.helm_chart_name} #mandatory
description: A Helm chart for Kubernetes
type: application
version: 0.1.0 #mandatory
appVersion: 1.0""")
    # installing the helm for first time
    subprocess.call(["helm", "install", project.helm_chart_name, project.helm_chart_path])

    LOGGER.info("project directories created..")
    project.save()
    return project


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


def delete_project(project_id):
    VERBOSE_LOGGER.info("Deleting a project started.")
    project = Project.objects.get(id=project_id)

    subprocess.call(["helm", "uninstall", project.helm_chart_name, project.helm_chart_path])
    for image in Image.objects.filter(project_id=project_id):
        subprocess.call(["docker", "rmi", image.name])
        image.delete()
        LOGGER.info(image.name + " has been deleted.")

    shutil.rmtree(project.directory)
    LOGGER.info("project deleted successfully.")


def start_monitoring(project_id):
    project = Project.objects.get(id=project_id)

    data_monitor(project)


def get_config_file(project_id, file_name):
    project = Project.objects.get(id=project_id)
    file_name = file_name + ".json"
    config = dict()
    for file in os.listdir(os.path.join(project.directory, NEW_CONFIG)):
        if file == file_name:
            with open(os.path.join(project.directory, NEW_CONFIG, file)) as config_file:
                config = json.load(config_file)
    return config
