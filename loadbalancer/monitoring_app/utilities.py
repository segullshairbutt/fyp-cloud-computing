import os
import subprocess
import logging

from django.conf import settings
VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stub(config_file, project_directory, pod_name="Pod1", **kwargs):
    VERBOSE_LOGGER.info("creating server stubs for provided template.")
    # it will give the config name from whole filepath only i-e 07config
    config_name = str(config_file.split('/')[-1]).split('.')[0]

    output_directory = os.path.join(project_directory, "server-stubs", config_name, pod_name)
    subprocess.call(
        ["java", "-jar", JAR_FILE_PATH, "generate", "-i", config_file, "-g", "spring", "-o", output_directory])

    # packaging the maven project
    LOGGER.info("packaging the maven application")
    subprocess.call(["mvn", "-f", output_directory, "package"])

    # creating a docker image file for this server stub
    with open(os.path.join(output_directory, "Dockerfile"), "w") as dockerfile:
        LOGGER.info("writting docker file.")
        dockerfile.write("""FROM openjdk:8-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]""")

    # building the docker image withe created file.
    docker_image_name = settings.DOCKER_IMAGE_NAME + f":{config_name.lower()}_{pod_name.lower()}_image"
    subprocess.call(["docker", "build", "-t", docker_image_name, output_directory])

    # pushing the image to docker hub
    subprocess.call(["docker", "push", docker_image_name])

    with(open(os.path.join(kwargs.get("helm_chart_path"), "Chart.yaml"), "w")) as chart_file:
        LOGGER.info("writing Chart.YAML file")
        chart_file.write(f"""apiVersion: v2 #mandatory
name: open-api-chart #mandatory
description: A Helm chart for Kubernetes
type: application
version: 0.1.0 #mandatory
appVersion: 1.{str(int(config_name.split("config")[0]))}""")

    with(open(os.path.join(kwargs.get("helm_chart_template_path"), "deployment.yaml"), "w")) as deployment_file:
        LOGGER.info("writing deployment.YAML file")
        deployment_file.write(f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: open-api-app-v-{str(int(config_name.split("config")[0]))}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: open-api-app-v-{str(int(config_name.split("config")[0]))}
  template:
    metadata:
      labels:
        app: open-api-app-v-{str(int(config_name.split("config")[0]))}
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
  name: open-api-app-v-{str(int(config_name.split("config")[0]))}
spec:
  selector:
    app: open-api-app-v-{str(int(config_name.split("config")[0]))}
  ports:
    - port: 8081
      targetPort: 8080          
  type: LoadBalancer""")

    subprocess.call(["helm", "upgrade", "open-api-app", kwargs.get("helm_chart_path")])
