import copy
import json
import logging
import os
import shutil
import subprocess
from os.path import basename
from zipfile import ZipFile

from django.conf import settings

from constants import ProjectPaths
from monitoring_app.models import Cluster, RefPath, Method
from monitoring_app.utilities import _gen_dict_extract, _get_schema_only, _get_schemas_only

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stubs(source_config_file_path, project_directory, **kwargs):
    new_config_files_path = os.path.join(project_directory, ProjectPaths.NEW_CONFIGS)
    if not os.path.isdir(new_config_files_path):
        os.makedirs(new_config_files_path)

    new_template_paths = _get_templates(source_config_file_path, new_config_files_path)
    for cl, wns in new_template_paths.items():
        for wn, pods in wns.items():
            for pod, single_container in pods.items():
                for container_name, config in single_container.items():
                    image_name = _create_server_stub(config["path"], project_directory, config["tag"] + "config", config["name"])
                    config["image"] = image_name
    count = 1

    # removing all deployments that are made before

    # _delete_folder_content(kwargs.get("helm_chart_template_path"))
    # helm_deployment_path = kwargs.get("helm_deployment_path")

    return new_template_paths
    # with ZipFile(os.path.join(helm_deployment_path, config_name), "w") as zip_obj:
    #     helm_chart_path = kwargs.get("helm_chart_path")
    #     for folder_name, sub_folder_name, file_names in os.walk(helm_chart_path):
    #         for file_name in file_names:
    #             file_path = os.path.join(folder_name, file_name)
    #             zip_obj.write(file_path, basename(file_path))
    # subprocess.call(["helm", "upgrade", "open-api-app", kwargs.get("helm_chart_path")])


def _create_server_stub(config_file, project_directory, config_tag, config_name):
    VERBOSE_LOGGER.info("creating server stub for provided template.")

    output_directory = os.path.join(project_directory, "server-stubs", config_tag, config_name)
    subprocess.call(
        ["java", "-jar", JAR_FILE_PATH, "generate", "-i", config_file, "-g", "spring", "-o", output_directory])

    # packaging the maven project
    LOGGER.info("packaging the maven application")
    subprocess.call(["mvn", "-f", output_directory, "package"])

    # creating a docker image file for this server stub
    with open(os.path.join(output_directory, "Dockerfile"), "w") as dockerfile:
        LOGGER.info("writing docker file.")

        dockerfile.write("""FROM openjdk:8-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]""")

    # building the docker image withe created file.
    docker_image_name = settings.DOCKER_IMAGE_NAME + f":{config_name.lower()}_image"
    subprocess.call(["docker", "build", "-t", docker_image_name, output_directory])

    # pushing the image to docker hub
    # subprocess.call(["docker", "push", docker_image_name])

    # version = str(int(config_name.split("config")[0].split("_")[1]))

    # helm_chart, helm_deployment = get_helm_chart(version, count, docker_image_name)
    # with(open(os.path.join(kwargs.get("helm_chart_path"), "Chart.yaml"), "w")) as chart_file:
    #     LOGGER.info("writing Chart.YAML file")
    #     chart_file.write(helm_chart)
    #
    # with(open(os.path.join(
    #         kwargs.get("helm_chart_template_path"), config_name.lower() + "deployment.yaml"
    # ), "w")) as deployment_file:
    #     LOGGER.info("writing deployment.YAML file")
    #     deployment_file.write(helm_deployment)
    return docker_image_name

def _get_method_by_ref(ref_path, methods):
    for method in methods:
        if method.ref_path.full_path == ref_path:
            return method
    return None


def _get_templates(config_file, new_config_directory):
    VERBOSE_LOGGER.info("Started creating templates.")

    file_tag = config_file.split('/')[-1].split('config.json')[0]

    with open(config_file, "r") as template_file:
        config_template = json.load(template_file)
        cluster_template = config_template['info']['x-clusters']
        name = next(iter(cluster_template))
        cluster = Cluster(name, 0, cluster_template[name], '#/info/x-clusters/' + name)

        schemas_template = config_template['components']['schemas']

        methods = []
        for path_name, path in config_template['paths'].items():
            for method_name, method in path.items():
                ref_path = RefPath(method[RefPath.X_LOCATION][RefPath.REF])
                all_references = list(set(_gen_dict_extract(RefPath.REF, method)))
                schema_name = _get_schema_only(all_references)

                methods.append(Method(path_name, method_name, ref_path, 0, schema_name, method))

        config_containers = {}
        for wn in cluster.worker_nodes:
            for pod in wn.pods:
                for container in pod.containers:
                    method = _get_method_by_ref(container.ref_path, methods)
                    if method:
                        config_container_ref = config_containers.setdefault(container.ref_path, {})
                        config_container_ref['container'] = container
                        config_container_ref_methods = config_container_ref.setdefault('methods', [])
                        config_container_ref_methods.append(method)

        new_templates = {}
        for path, config_container in config_containers.items():
            copied_template = copy.deepcopy(config_template)
            ref_path = RefPath(path)
            container_obj = config_container['container']
            container = {container_obj.name: container_obj.full_component}

            # keeping only current worker-node
            wn_template = copied_template[ref_path.INFO][ref_path.X_CLUSTERS][ref_path.cluster][ref_path.WORKER_NODES]
            wn_template = {ref_path.worker_node: wn_template[ref_path.worker_node]}
            # keeping only current pod
            pods_template = wn_template[ref_path.worker_node][ref_path.PODS]
            pods_template = {ref_path.pod_name: pods_template[ref_path.pod_name]}
            # keeping only current container
            pods_template[ref_path.pod_name][ref_path.CONTAINERS] = container

            wn_template[ref_path.worker_node][ref_path.PODS] = pods_template
            copied_template[ref_path.INFO][ref_path.X_CLUSTERS][ref_path.cluster][ref_path.WORKER_NODES] = wn_template

            paths = {}
            schemas = {}
            # getting all schemas which are referenced to the methods
            for method in config_container['methods']:
                methods_config = paths.setdefault(method.path_name, {})
                methods_config[method.method_name] = method.full_method
                if method.schema_name != 'default':
                    schemas[method.schema_name] = schemas_template[method.schema_name]

            # getting all those schemas which have ref to any schema of methods
            referenced_schemas = {}
            for name, schema in schemas.items():
                all_references = list(set(_gen_dict_extract('$ref', schema)))
                schema_names = _get_schemas_only(all_references)
                for schema_name in schema_names:
                    referenced_schemas[schema_name] = schemas_template[schema_name]
            schemas.update(referenced_schemas)

            copied_template['paths'] = paths
            copied_template['components']['schemas'] = schemas

            new_cluster_template = new_templates.setdefault(ref_path.cluster, {})
            new_wn_template = new_cluster_template.setdefault(ref_path.worker_node, {})
            new_pod_template = new_wn_template.setdefault(ref_path.pod_name, {})
            new_pod_template[ref_path.container_name] = copied_template

        new_paths_template = copy.deepcopy(new_templates)
        for cl, wns in new_templates.items():
            for wn, pods in wns.items():
                for pod, single_container in pods.items():
                    for container_name, config in single_container.items():
                        output_name = f"{file_tag}_{cl}_{wn}_{pod}_{container_name}"
                        output_file_name = output_name + ".json"
                        output_file_path = os.path.join(new_config_directory, output_file_name)

                        with open(output_file_path, "w") as output_file:
                            json.dump(config, output_file, indent=2)

                        new_paths_template[cl][wn][pod][container_name] = {"name": output_name,
                                                                           "path": output_file_path,
                                                                           "tag": file_tag}

        return new_paths_template


def _delete_folder_content(folder):
    VERBOSE_LOGGER.info("removing content from helm charts.")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            LOGGER.error('Failed to delete %s. Reason: %s' % (file_path, e))
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_helm_chart(version, count, image_name):
    deployment_file = f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: open-api-app-v-{version}-{str(count)}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: open-api-app-v-{version}-{str(count)}
  template:
    metadata:
      labels:
        app: open-api-app-v-{version}-{str(count)}
    spec:
      containers:
        - name: app
          image: {image_name}
          ports:
            - containerPort: 8080          
          imagePullPolicy: IfNotPresent
---
apiVersion: v1
kind: Service
metadata:
  name: open-api-app-v-{version}-{str(count)}
spec:
  selector:
    app: open-api-app-v-{version}-{str(count)}
  ports:
    - port: 8081
      targetPort: 8080          
  type: LoadBalancer"""

    chart_file = f"""apiVersion: v2 #mandatory
name: open-api-chart #mandatory
description: A Helm chart for Kubernetes
type: application
version: 0.1.0 #mandatory
appVersion: 1.{version}.{str(count)}"""

    return chart_file, deployment_file
