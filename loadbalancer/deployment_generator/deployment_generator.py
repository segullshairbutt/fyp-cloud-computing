import copy
import json
import os
import shutil
import zipfile
import logging

import yaml

from deployment_generator.deployment_file_templates import (get_initial_service_content,
                                                            get_initial_deployment_content,
                                                            get_container_template,
                                                            get_docker_image, get_service_template,
                                                            get_values_file_content,
                                                            get_chart_file_content,
                                                            get_deployment_file_content, get_services_template)

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def generate_docker_yaml_files(
        tag, expose_port, docker_deployment_path, configuration, yaml_filepath):
    VERBOSE_LOGGER.info("generating docker & yaml files.")

    container_counter = 1
    services_counter = 1
    for content in configuration:
        for container in content['pod']['containers']:
            deployment_name = "nodeapp-{}-{}".format(str(tag), str(container_counter))

            deployment_services = get_initial_service_content(deployment_name)

            deployment = get_initial_deployment_content(deployment_name)

            container_template = get_container_template()

            docker_image_content = get_docker_image(expose_port)

            services_template = get_service_template()

            for service in container['services']:
                services_template['name'] = "service{}".format(services_counter)
                services_template['port'] = int(service['port'])
                services_template['targetport'] = expose_port
                deployment_services['spec']['ports'].append(copy.deepcopy(services_template))
                services_counter = services_counter + 1

            container_template["container"] = "container-{}".format(container_counter)
            container_template["image"] = "image-{}".format(container_counter)
            container_template["ports"]["-containerPort"] = expose_port

            deployment['spec']['template']['spec']['containers'].append(copy.deepcopy(container_template))

            docker_file_name = str(tag) + '-' + str(container_counter) + '.Dockerfile'

            docker_file_path = os.path.join(docker_deployment_path, docker_file_name)
            with open(docker_file_path, 'w') as dockerFile:
                dockerFile.write(docker_image_content)
                LOGGER.info("docker image file written.")

            with open(os.path.join(yaml_filepath, str(tag) + "-" + str(container_counter) + "services.yaml"),
                      "w") as file:
                yaml.dump(deployment_services, file)
                LOGGER.info("deployment services file written.")

            with open(os.path.join(yaml_filepath, str(tag) + "-" + str(container_counter) + "deployment.yaml"),
                      "w") as file:
                yaml.dump(deployment, file)
                LOGGER.info("deployment file written.")

            container_counter = container_counter + 1


def generate_helm_deployments(tag, configuration, docker_image, expose_ports, helm_deployment_path):
    VERBOSE_LOGGER.info("generating helm deployment files.")
    for content in configuration:
        container_counter = 1

        for container in content['pod']['containers']:
            file_tags = '{}-{}'.format(tag, container_counter)
            deployment_name = 'nodeapp-{}'.format(file_tags)
            helm_chart_path = os.path.join(helm_deployment_path, file_tags + "-chart")
            container_counter = container_counter + 1
            template_dir = os.path.join(helm_chart_path, '../monitoring_app/templates')
            os.makedirs(template_dir)

            # writing values.yaml file
            with open(os.path.join(helm_chart_path, 'values.yaml'), "w") as file:
                file.write(get_values_file_content(docker_image, expose_ports, deployment_name))
                LOGGER.info("values.yaml files written..")

            # writing chart.yaml file
            with open(os.path.join(helm_chart_path, 'Chart.yaml'), "w") as file:
                file.write(get_chart_file_content(deployment_name))
                LOGGER.info("chart.yaml files written..")

            services_path = os.path.join(template_dir, 'service.yaml')
            deployment_path = os.path.join(template_dir, 'deployment.yaml')

            # writing deployment.yaml file
            with open(deployment_path, "w") as file:
                file.write(get_deployment_file_content(deployment_name))
                LOGGER.info("deployment.yaml files written..")

            # write services.yaml file
            services = get_services_template()

            services_port_template = {
                "protocol": "TCP",
                "name": 0,
                "port": 0000,
                "targetPort": "{{ .Values.service.targetPort }}"
            }

            services_counter = 1
            for service in container["services"]:
                services_port_template['port'] = int(service['port'])
                services_port_template['name'] = "service-" + str(services_counter)
                services['spec']['ports'].append(copy.deepcopy(services_port_template))
                services_counter = services_counter + 1

            with open(services_path, "w") as file:
                yaml.dump(services, file)
                LOGGER.info("services are written to")

            # creating the zip file
            zip_path = os.path.join(helm_deployment_path, file_tags + '-chart.zip')
            generated_zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(helm_chart_path):
                for file in files:
                    generated_zip.write(os.path.join(root, file))
            generated_zip.close()

            shutil.rmtree(helm_chart_path)


def generate_deployment_files(tag, filepaths):
    VERBOSE_LOGGER.info("Generating deployment files.")

    filename = str(tag) + 'config.json'
    filepath = os.path.join(filepaths.config_data_path, filename)
    # reading the configuration file
    with open(filepath) as f:
        data = f.read()
        configuration = json.loads(data)

    # creating the expose port from  default clone project's dockerfile
    expose_port = 3000  # default port
    # open docker file to get expose port
    with open(filepaths.default_docker_filepath, "r") as dockerfile:
        for content in dockerfile:
            if "EXPOSE" in content:
                # getting expose port from DOCKERFILE
                expose_port = int(content.split()[1])

    generate_docker_yaml_files(tag, expose_port, filepaths.docker_deployment_path, configuration,
                               filepaths.yaml_filepath)
    generate_helm_deployments(tag, configuration, filepaths.docker_image, expose_port, filepaths.helm_deployment_path)
