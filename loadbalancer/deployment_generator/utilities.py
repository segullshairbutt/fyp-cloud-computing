import copy
import json
import logging
import os
import shutil
import subprocess
import javaproperties
from os.path import basename
from zipfile import ZipFile

from django.conf import settings
from django.db import transaction

from constants import ProjectPaths
from deployment_generator.models import Node, Image
from deployment_generator.templates import get_deployment_template
from monitoring_app.models import Cluster, RefPath, Method
from monitoring_app.utilities import gen_dict_extract, get_schema_only, get_schemas_only


VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")

JAR_FILE_PATH = os.path.join(str(os.getcwd()).split("/loadbalancer")[0], "openapi-generator-cli.jar")


def create_server_stubs(app_name, project_id, source_config_file_path, project_directory, helm_chart_name):
    VERBOSE_LOGGER.info("Creating server stubs started.")

    new_config_files_path = os.path.join(project_directory, ProjectPaths.NEW_CONFIGS)
    if not os.path.isdir(new_config_files_path):
        os.makedirs(new_config_files_path)

    new_template_paths = _get_templates(source_config_file_path, new_config_files_path)

    # making all images deployed already vanished so that they can be deleted after helm update
    with transaction.atomic():
        for image in Image.objects.filter(project_id=project_id):
            image.status = image.VANISH_ABLE
            image.save()

    # creating the server stubs
    config_tag = None
    for cl, wns in new_template_paths.items():
        for wn, pods in wns.items():
            for pod, single_container in pods.items():
                port = 8080

                for container_name, config in single_container.items():
                    context_path = f"demo-{str(port)[-1:]}"

                    image_name = _create_server_stub(
                        app_name, project_id, config["path"], project_directory, config["tag"] + "config",
                        config["name"], port, context_path=context_path)

                    config["image"] = image_name
                    config["port"] = port
                    config["context_path"] = context_path
                    config_tag = config["tag"]

                    port += 1

    # creating the helm templates
    templates = ""
    for cl_name, cluster in new_template_paths.items():
        count = 0
        for wn_name, pods in cluster.items():
            count += 1
            for pod_name, containers in pods.items():
                containers = list(containers.values())
                if containers:
                    templates = templates + get_deployment_template(
                        app_name, containers, wn_name, count) + "\n"

    # removing all deployments that are made before
    helm_chart_template_path = os.path.join(project_directory, ProjectPaths.HELM_CHARTS, ProjectPaths.TEMPLATES)
    _delete_folder_content(helm_chart_template_path)

    # dumping the yaml deployments to file
    with open(os.path.join(helm_chart_template_path, "All Deployments.yaml"), "w") as output_file:
        output_file.write(templates)
    helm_deployment_path = os.path.join(project_directory, ProjectPaths.HELM_DEPLOYMENTS)

    # creating zip of current configurations
    helm_chart_path = os.path.join(project_directory, ProjectPaths.HELM_CHARTS)
    with ZipFile(os.path.join(helm_deployment_path, str(config_tag) + "config"), "w") as zip_obj:
        LOGGER.info("Creating zip file for Helm Chart and Templates.")
        for folder_name, sub_folder_name, file_names in os.walk(helm_chart_path):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                zip_obj.write(file_path, basename(file_path))

    create_kubernetes_nodes(list(new_template_paths[next(iter(new_template_paths))].keys()))

    # pushing newly created images
    # push_new_images(project_id)

    subprocess.call(["helm", "upgrade", helm_chart_name, helm_chart_path])

    # vanishing the images which has been set to Vanish_able.
    vanish_images(project_id)

    LOGGER.info("Getting the service url and adding it to template")
    for cl, wns in new_template_paths.items():
        for wn, pods in wns.items():
            for pod, single_container in pods.items():
                for container_name, config in single_container.items():
                    print("CONTAINER NAME: " + config["name"])
                    cmd = ["minikube", "service", f"service-{config['name'].replace('_', '-')}", "--url"]
                    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
                    service_url = output.strip()

                    LOGGER.info(f"url for service-{config['name'].replace('_', '-')} is {service_url}")
                    with open(os.path.join(new_config_files_path, config["name"] + ".json"), "r+") as template_file:
                        template_data = json.load(template_file)
                        url = service_url.decode("utf-8")
                        template_data["servers"][0]["url"] = f"{url}/{config['context_path']}/"

                        template_file.seek(0)

                        json.dump(template_data, template_file, indent=4)
                        template_file.truncate()


def create_kubernetes_nodes(worker_nodes):
    difference = Node.objects.count() - len(worker_nodes)

    # here we are making the equal number of nodes which are required
    if difference < 0:
        # it means that we need more nodes
        for a in range(abs(difference)):
            subprocess.call(["minikube", "node", "add"])
            latest_node = Node.objects.last()
            new_node = Node()
            if latest_node:
                new_node.number = latest_node.number + 1
            else:
                new_node.number = 2

            new_node.name = "minikube-m0" + str(new_node.number)
            new_node.save()
    else:
        # getting the latest node and deleting them n time.
        for a in range(difference):
            node = Node.objects.last()
            subprocess.call(["minikube", "node", "delete", node.name])
            node.delete()

    # as number of worker_nodes and saved nodes is same so we have can iterate over both arrays
    for index in range(len(worker_nodes)):
        worker_node = worker_nodes[index]
        node = Node.objects.all()[index]
        subprocess.call(["kubectl", "label", "nodes", node.name, "name=" + worker_node, "--overwrite"])
        # here we will label the nodes with their names
        print(worker_node, node.name)


def _create_server_stub(
        app_name, project_id, config_file, project_directory, config_tag, config_name, port, context_path):
    VERBOSE_LOGGER.info("creating server stub for provided template.")

    output_directory = os.path.join(project_directory, "server-stubs", config_tag, config_name)
    subprocess.call(
        ["java", "-jar", JAR_FILE_PATH, "generate", "-i", config_file, "-g", "spring", "-o", output_directory])

    # changing the port of application in application.properties file
    prop_file_path = find_file_path("application.properties", output_directory)

    with open(prop_file_path, "w+") as prop_file:
        all_props = javaproperties.load(prop_file)
        port = str(port)
        all_props["server.port"] = port
        all_props["server.servlet.context-path"] = f"/{context_path}/"
        javaproperties.dump(all_props, prop_file)

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
    docker_image_name = settings.DOCKER_IMAGE_NAME + f":{app_name.replace('-', '_')}_{config_name.lower()}_image"
    subprocess.call(["docker", "build", "-t", docker_image_name, output_directory])

    # pushing the image to docker hub
    Image.objects.create(name=docker_image_name, project_id=project_id)
    return docker_image_name


def push_new_images(project_id):
    for image in Image.objects.filter(status=Image.PENDING, project_id=project_id):
        subprocess.call(["docker", "push", image.name])
        image.status = image.PUSHED
        image.save()
        LOGGER.info(image.name + " has been pushed.")


def vanish_images(project_id):
    for image in Image.objects.filter(status=Image.VANISH_ABLE, project_id=project_id):
        subprocess.call(["docker", "rmi", image.name])
        image.delete()
        LOGGER.info(image.name + " has been vanished.")


def _get_methods_by_ref(ref_path, methods):
    reference_methods = []
    for method in methods:
        if method.ref_path.full_path == ref_path:
            reference_methods.append(method)
    return reference_methods


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
                all_references = list(set(gen_dict_extract(RefPath.REF, method)))
                schema_name = get_schema_only(all_references)

                methods.append(Method(path_name, method_name, ref_path, 0, schema_name, method))
        LOGGER.info("Total methods: " + str(len(methods)))

        config_containers = {}
        for wn in cluster.worker_nodes:
            for pod in wn.pods:
                for container in pod.containers:
                    config_container_ref = config_containers.setdefault(container.ref_path, {})
                    config_container_ref['container'] = container
                    config_container_ref['methods'] = _get_methods_by_ref(container.ref_path, methods)

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
            for ref_method in config_container['methods']:
                methods_config = paths.setdefault(ref_method.path_name, {})
                methods_config[ref_method.method_name] = ref_method.full_method
                if ref_method.schema_name != 'default':
                    schemas[ref_method.schema_name] = schemas_template[ref_method.schema_name]

            # getting all those schemas which have ref to any schema of methods
            referenced_schemas = {}
            for name, schema in schemas.items():
                all_references = list(set(gen_dict_extract('$ref', schema)))
                schema_names = get_schemas_only(all_references)
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
                                                                           "tag": file_tag
                                                                           }

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


def find_file_path(filename, search_path):
    for root, directory, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
