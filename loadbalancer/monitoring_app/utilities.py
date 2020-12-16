import os
import subprocess

from django.conf import settings

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stub(config_file, project_directory, pod_name="Pod1"):
    # it will give the config name from whole filepath only i-e 07config
    config_name = str(config_file.split('/')[-1]).split('.')[0]

    output_directory = os.path.join(project_directory, "server-stubs", config_name, pod_name)
    subprocess.call(
        ["java", "-jar", JAR_FILE_PATH, "generate", "-i", config_file, "-g", "spring", "-o", output_directory])

    # packaging the maven project
    subprocess.call(["mvn", "-f", output_directory, "package"])

    # creating a docker image file for this server stub
    with open(os.path.join(output_directory, "Dockerfile"), "w") as dockerfile:
        dockerfile.write("""FROM openjdk:8-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]""")

    # building the docker image withe created file.
    docker_image_name = settings.DOCKER_IMAGE_NAME + f":{config_name.lower()}_{pod_name.lower()}_image"
    subprocess.call(["docker", "build", "-t", docker_image_name, output_directory])
