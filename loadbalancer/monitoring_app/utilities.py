import copy
import json
import logging
import os
import shutil
import subprocess

from django.conf import settings

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stubs(source_config_file, project_directory, **kwargs):
    config_files = _get_templates(source_config_file, project_directory)
    count = 1

    # removing all deployments that are made before
    _delete_folder_content(kwargs.get("helm_chart_template_path"))

    for config_file in config_files:
        _create_server_stub(config_file, project_directory, count, **kwargs)
        count += 1

    subprocess.call(["helm", "upgrade", "open-api-app", kwargs.get("helm_chart_path")])


def _create_server_stub(config_file, project_directory, count, **kwargs):
    VERBOSE_LOGGER.info("creating server stub for provided template.")
    # it will give the config name from whole filepath only i-e 07config
    config_name = str(config_file.split('/')[-1]).split('.')[0]

    output_directory = os.path.join(project_directory, "server-stubs", config_name)
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
    subprocess.call(["docker", "push", docker_image_name])

    version = str(int(config_name.split("config")[0].split("_")[1]))

    with(open(os.path.join(kwargs.get("helm_chart_path"), "Chart.yaml"), "w")) as chart_file:
        LOGGER.info("writing Chart.YAML file")
        chart_file.write(f"""apiVersion: v2 #mandatory
name: open-api-chart #mandatory
description: A Helm chart for Kubernetes
type: application
version: 0.1.0 #mandatory
appVersion: 1.{version}.{str(count)}""")

    with(open(os.path.join(
            kwargs.get("helm_chart_template_path"), config_name.lower() + "deployment.yaml"
    ), "w")) as deployment_file:
        LOGGER.info("writing deployment.YAML file")
        deployment_file.write(f"""---
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
          image: {docker_image_name}
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
  type: LoadBalancer""")


def _get_templates(config_file, project_directory):
    VERBOSE_LOGGER.info("Started creating templates.")

    with open(config_file, "r") as template_file:
        template = json.load(template_file)
        methods = []
        for path_name, path in template["paths"].items():
            for method_name, method in path.items():
                ref_path = RefPath(method["x-location"]["$ref"])
                full_method = dict()
                full_method[method_name] = method
                methods.append(Method(path_name, method_name, ref_path, full_method))

        pods = []
        for pod_name, pod in template["info"]["x-pods"].items():
            full_pod = dict()
            full_pod[pod_name] = pod
            pods.append(Pod(pod_name, full_pod))
        templates = []

        count = 1
        for pod in pods:
            sample_template = copy.deepcopy(template)
            pod_methods = {}
            for method in methods:
                if method.ref_path.pod_name == pod.pod_name:
                    pod_methods[method.path_name] = method.full_method
            if len(pod_methods):
                sample_template["info"]["x-pods"] = pod.full_pod
                sample_template["paths"] = pod_methods

                config_name = str(config_file.split('/')[-1]).split('.')[0]
                config_name = str(count) + "_" + config_name + ".json"
                new_configs_path = os.path.join(project_directory, "new_configs")
                if not os.path.isdir(new_configs_path):
                    os.makedirs(new_configs_path)

                file_path = os.path.join(new_configs_path, config_name)
                with open(file_path, "w") as new_file:
                    json.dump(sample_template, new_file)
                    templates.append(file_path)

                LOGGER.info(str(len(pod_methods)) + " endpoint methods appended to " + pod.pod_name)

            count += 1
        return templates


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


class Method:
    def __init__(self, path_name, method_name, ref_path, full_method):
        self.path_name = path_name
        self.method_name = method_name
        self.ref_path = ref_path
        self.full_method = full_method

    def __str__(self):
        return self.path_name + ": " + self.method_name + " (" + self.ref_path.full_path + ")"


class Pod:
    def __init__(self, pod_name, full_pod):
        self.pod_name = pod_name
        self.full_pod = full_pod


class RefPath:
    def __init__(self, ref_path):
        paths = ref_path.split("#/info/x-pods/")
        parts = paths[1].split("/")
        self.pod_name = parts[0]
        self.container_name = parts[2]

    @property
    def full_path(self):
        return "#/info/x-pods/" + self.pod_name + "/containers/" + self.container_name + "/port"
