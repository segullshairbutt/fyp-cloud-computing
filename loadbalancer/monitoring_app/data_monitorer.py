import copy
import json
import logging
import os

import monitoring_app.data_generator as data_generator
import monitoring_app.templates.config_templates as config_templates
from monitoring_app.constants import MAX_WN_LOAD, MAX_POD_LOAD
from monitoring_app.models import Cluster, ContainerGroup, MethodGroup, PodGroup, RefPath, Method
from monitoring_app.utilities import _join_components, _gen_dict_extract, _get_schema_only

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def _get_config_file(filepath):
    VERBOSE_LOGGER.info("getting config file.")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read()
        dataset = json.loads(data)
    return dataset


def _write_config_file(template, dir_path, filename):
    VERBOSE_LOGGER.info("generating config file.")
    print('filename is ', filename)
    path = os.path.join(dir_path, filename)
    print('writing config file../.')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)


def _get_total_files_length(dir_path):
    dir_size = (len(os.listdir(dir_path)))
    # as it contains config and data files
    total_files = int(dir_size / 2)

    return total_files


def _get_new_filetag(dir_path):
    """This method will return integer that is the number for new next file
     in that directory"""

    dir_size = (len(os.listdir(dir_path)))
    dir_size = int(dir_size / 2)
    new_file_tag = dir_size + 1
    if new_file_tag < 10:
        new_file_tag = str("0" + str(new_file_tag))
    return new_file_tag


def _get_latest_filetag(dir_path):
    """get the number of latest configuration file"""

    dir_size = (len(os.listdir(dir_path)))
    file_tag = int(dir_size / 2)
    if file_tag < 10:
        file_tag = str("0" + str(file_tag))
    return file_tag


def _generate_related_data(dir_path, config_file, data_file_name):
    """Get the latest min and max ranges for cpu

    Container and services need this method, because we have to generate new data for the same
    file if monitoring algorithm did not found any exceeding threshold in the specific data.
    Json file new data depend on the previous data last object because in real time there is
    very small variation in resource usage
    """
    VERBOSE_LOGGER.info("getting latest data.")

    with open(os.path.join(dir_path, data_file_name), 'r') as data:
        data_file_content = json.loads(data.read())
        data_file_content = data_file_content[len(data_file_content) - 1]

        cluster = data_file_content["x-clusters"][next(iter(data_file_content["x-clusters"]))]
        cl_load = cluster["metrics"]["load"]

        worker_node = cluster['worker-nodes'][next(iter(cluster['worker-nodes']))]
        wn_load = worker_node['metrics']['load']

        pod = worker_node['pods'][next(iter(worker_node['pods']))]
        pod_load = pod['metrics']['load']

        container = pod['containers'][next(iter(pod['containers']))]
        container_load = container['metrics']['load']

        first_path_key = next(iter(data_file_content["paths"]))
        first_method_key = next(iter(data_file_content["paths"][first_path_key]))

        method_load = data_file_content["paths"][first_path_key][first_method_key]["x-metrics"]["load"]

        kwargs = {
            "cl_load": cl_load,
            "wn_load": wn_load,
            "pod_load": pod_load,
            "container_load": container_load,
            "method_load": method_load
        }

        print("--------------------------DONE--------------------------")
        # config_and_metrics_generator.generate_data(dir_path, config_file, data_file, **kwargs)
        data_generator.generate_data(dir_path, config_file, data_file_name, **kwargs)


def data_monitor(project):
    VERBOSE_LOGGER.info("data-monitor started.")

    config_dir_path = project.config_data_path

    # generating a new file if already doesn't exists
    if _get_total_files_length(config_dir_path) == 0:
        # generated_template = generate_configuration_template(end_points)
        initial_template = config_templates.generate_configuration(project.path_urls.all())
        LOGGER.info("Generating initial files")

        # getting all methods from a fat container
        methods = []
        for path_name, path in initial_template["paths"].items():
            for method_name, method in path.items():
                ref_path = RefPath(method["x-location"]["$ref"])

                all_references = list(set(_gen_dict_extract('$ref', method)))
                schema_name = _get_schema_only(all_references)

                methods.append(Method(path_name, method_name, ref_path, '', schema_name, method))

        schema_grouped_methods = {}
        for method in methods:
            schema_grouped_methods.setdefault(method.schema_name, [])
            schema_grouped_methods[method.schema_name].append(method)

        index = 1
        copied_template = copy.deepcopy(initial_template)
        for schema_name, schema_methods in schema_grouped_methods.items():
            if index == 1:
                pass
            else:
                first_method = schema_methods[0]
                new_container = "c" + str(index)

                container_template = {'id': new_container, 'metrics': {'load': ''}}
                ref_path = first_method.ref_path
                copied_template["info"]["x-clusters"][ref_path.cluster]["worker-nodes"][ref_path.worker_node]["pods"][
                    ref_path.pod_name]["containers"][new_container] = container_template

                for method in schema_methods:
                    method.ref_path.container_name = new_container
                    method.full_method["x-location"]["$ref"] = method.ref_path.full_path
                    copied_template["paths"][method.path_name][method.method_name] = method.full_method
            index += 1

        # generate the name for new configuration file
        configfile = str(_get_new_filetag(config_dir_path)) + 'config.json'
        # generate the name for new data file
        datafile = str(_get_new_filetag(config_dir_path)) + 'data.json'
        # populate new configuration file
        _write_config_file(copied_template, config_dir_path, configfile)
        # populate new data file
        # config_and_metrics_generator.generate_data(config_dir_path, configfile, datafile)
        data_generator.generate_data(config_dir_path, configfile, datafile)

        # creating the server side code
        # utilities.create_server_stubs(
        #     os.path.join(project.config_data_path, configfile),
        #     project.directory,
        #     helm_chart_path=project.helm_chart_path,
        #     helm_chart_template_path=project.helm_chart_templates_path,
        #     helm_deployment_path=project.helm_deployment_path
        # )

    for run in range(1):
        latest_filetag = str(_get_latest_filetag(config_dir_path))
        data_read_file = latest_filetag + 'data.json'
        data_read_path = os.path.join(config_dir_path, data_read_file)
        with open(data_read_path) as f:
            data = f.read()
            dataset = json.loads(data)

        # call monitoring function to check whether data.json file have any object that exceeds
        # threshold, if yes then we need to update the template (config.json file)
        new_template = _monitor_scaling(dataset, config_dir_path)
        # if false then no change in template occur after monitoring , need to add more objects to the latest
        # data.json file

        if not new_template:
            # no need to update the template just overwrite the new data to latest data.json file
            # add more objects to the latest data.json file
            data_file = str(_get_latest_filetag(config_dir_path)) + 'data.json'
            config_file = str(_get_latest_filetag(config_dir_path)) + 'config.json'
            _generate_related_data(config_dir_path, config_file, data_file)

            LOGGER.info("no changing in template no need to update the config file")
            continue
        else:
            print('--------------------------')
            VERBOSE_LOGGER.info("changes detected, trying to create new configuration")
            # how much containers we need for new template (config.json file)
            LOGGER.info('Total pods: {}'.format(len(new_template["info"]["x-pods"])))

            print('--------------------------')
            # generate stuff for new files

            # creating name for new configuration file
            new_config_file = str(_get_new_filetag(config_dir_path)) + 'config.json'

            # creating name for new data file
            new_data_file = str(_get_new_filetag(config_dir_path)) + 'data.json'

            # creating config.json file with new template
            _write_config_file(new_template, config_dir_path, new_config_file)

            # creating the data.json file populate data according to new template
            data_generator.generate_data(config_dir_path, new_config_file, new_data_file)

            # creating the server side code
            # utilities.create_server_stubs(
            #     os.path.join(project.config_data_path, new_config_file),
            #     project.directory,
            #     helm_chart_path=project.helm_chart_path,
            #     helm_chart_template_path=project.helm_chart_templates_path,
            #     helm_deployment_path=project.helm_deployment_path
            # )

            """create docker files according to how many containers we need in new config
            we are passing prev_files_tags here because at last 2 function that we call above
            already created new files"""

            # generate_deployment_files(config_and_metrics_generator.get_latest_filetag(config_dir_path), paths)


def _derive_components(single_data_obj):
    clusters = []
    cls = single_data_obj["x-clusters"]

    for cl in cls.values():
        ref_path = RefPath.INITIAL + cl["name"]
        clusters.append(Cluster(cl["name"], cl["metrics"]["load"], cl, ref_path))

    methods = []
    data_paths = single_data_obj["paths"]
    for path_name, path in data_paths.items():
        for method_name, method in path.items():
            ref_path = RefPath(method["x-location"]["$ref"])

            all_references = list(set(_gen_dict_extract('$ref', method)))
            schema_name = _get_schema_only(all_references)

            methods.append(
                Method(path_name, method_name, ref_path, method["x-metrics"]["load"], schema_name, method))
    return clusters, methods


def _get_scalable_components(clusters):
    scalable_wns = []
    scalable_pods = []
    for cluster in clusters:
        for worker_node in cluster.worker_nodes:
            if worker_node.load < MAX_WN_LOAD:
                print("no need to scale ", str(worker_node))

                for wn_pod in worker_node.pods:
                    if wn_pod.load < MAX_POD_LOAD:
                        print("no need to scale", str(wn_pod))
                    else:
                        print(wn_pod, " need scaling.")
                        scalable_pods.append(wn_pod)
            else:
                print(worker_node, " need scaling.")
                scalable_wns.append(worker_node)
    return scalable_wns, scalable_pods


def _get_pod_groups(scalable_wns):
    pod_groups = []
    for wn in scalable_wns:
        sum_of_pod_loads = sum(p.load for p in wn.pods)
        pod_groups.append(PodGroup(wn.load, sum_of_pod_loads, wn.pods))
    return pod_groups


def _get_container_groups(scalable_pods):
    container_groups = []
    for scalable_pod in scalable_pods:
        sum_of_container_loads = sum(c.load for c in scalable_pod.containers)
        container_groups.append(
            ContainerGroup(scalable_pod.load, sum_of_container_loads, scalable_pod.containers))
    return container_groups


def _monitor_scaling(config_data, config_path):
    VERBOSE_LOGGER.info("Monitor the scaling of pods and containers.")

    file_name = str(_get_latest_filetag(config_path)) + "config.json"
    template = copy.deepcopy(_get_config_file(os.path.join(config_path, file_name)))
    copied_template = copy.deepcopy(template)

    for single_data_object in config_data:
        # converting provided data to objects
        clusters, methods = _derive_components(single_data_object)

        scalable_wns, scalable_pods = _get_scalable_components(clusters)

        # monitoring based on pods
        monitor_pods(_get_container_groups(scalable_pods), methods, copied_template)
        # scaling based upon the worker-nodes
        _monitor_worker_nodes(_get_pod_groups(scalable_wns), methods, clusters[0], copied_template)

        if copied_template == template:
            print("no changes detected to template.")
        else:
            print("returning new template")
            return copied_template

    # if no new template is made None type is returned back
    return None


def _monitor_worker_nodes(pod_groups, methods, cluster, copied_template):
    for group in pod_groups:
        print("entered in monitoring the pod groups.")
        joined_pods, remaining_pods = _join_components(MAX_WN_LOAD, group.get_contributed_components())

        # getting first pod from remaining pods
        first_remaining_pod = remaining_pods[0]
        sum_of_container_loads = sum(c.load for c in first_remaining_pod.containers)
        container_group = ContainerGroup(first_remaining_pod.load, sum_of_container_loads, first_remaining_pod.containers)

        sum_of_joined_pods_contribution = sum(j_p.contribution for j_p in joined_pods)
        joined_containers, remaining_containers = _join_components(
            (MAX_WN_LOAD - sum_of_joined_pods_contribution), container_group.get_contributed_components())

        # getting first container from remaining containers
        next_joining_container = remaining_containers[0]

        next_joining_container_methods = []
        for method in methods:
            if method.ref_path.full_path == next_joining_container.ref_path:
                next_joining_container_methods.append(method)
        sum_of_method_loads = sum(m.load for m in next_joining_container_methods)
        method_group = MethodGroup(next_joining_container.load, sum_of_method_loads, next_joining_container_methods)
        sum_of_joined_containers_contribution = sum(j_c.contribution for j_c in joined_containers)
        joined_methods, remaining_methods = _join_components(
            MAX_WN_LOAD - sum_of_joined_pods_contribution - sum_of_joined_containers_contribution,
            method_group.get_contributed_components())

        new_worker_node = None
        wn_name = "wn" + str(len(cluster.worker_nodes) + 1)
        if remaining_pods or remaining_containers or remaining_methods:
            print("create a new WN", wn_name)
            new_worker_node = {
                "name": wn_name,
                "metrics": {"load": ""},
                "pods": {}
            }

        new_pod = None
        pod_name = "pod" + str(len(remaining_pods[1:]) + 1)
        if remaining_methods or remaining_containers[1:]:
            print("creating a new POD", pod_name)
            new_pod = {
                "name": "pod1",
                "metrics": {
                    "load": ""
                }, "containers": {}
            }

        #         it means that all containers in first pod needs to get in new WN
        remaining_pods_to_deploy = remaining_pods if len(joined_containers) == 0 else remaining_pods[1:]

        if remaining_pods_to_deploy:
            print("create a new worker-node and add the pods in it.")
            for r_pod in remaining_pods_to_deploy:
                for r_container in r_pod.containers:
                    r_container_ref_path = RefPath(r_container.ref_path)
                    r_container_ref_path.pod_name = pod_name
                    r_container_ref_path.worker_node = wn_name

                    for method in methods:
                        if method.ref_path.full_path == r_container.ref_path:
                            method.ref_path = r_container_ref_path
                            ind_method = copied_template[RefPath.PATHS][method.path_name][method.method_name]
                            ind_method[RefPath.X_LOCATION][RefPath.REF] = r_container_ref_path.full_path

                            print(method)

                    # also replacing the path of container
                    r_container.ref_path = r_container_ref_path.full_path

        remaining_containers_to_deploy = remaining_containers if len(joined_methods) == 0 else remaining_containers[1:]
        if remaining_containers_to_deploy:
            print("create a new pod and add the containers in it.")
            for r_container in remaining_containers_to_deploy:
                r_container_ref_path = RefPath(r_container.ref_path)
                r_container_ref_path.pod_name = pod_name
                r_container_ref_path.worker_node = wn_name

                # replacing the path of methods
                for method in methods:
                    if method.ref_path.full_path == r_container.ref_path:
                        method.ref_path = r_container_ref_path
                        ind_method = copied_template[RefPath.PATHS][method.path_name][method.method_name]
                        ind_method[RefPath.X_LOCATION][RefPath.REF] = r_container_ref_path.full_path

                        print(method)

                # also replacing the path of container
                r_container.ref_path = r_container_ref_path.full_path

        cluster_template = copied_template[RefPath.INFO][RefPath.X_CLUSTERS][cluster.name][RefPath.WORKER_NODES]

        if new_worker_node:
            cluster_template[wn_name] = new_worker_node
            if new_pod:
                cluster_template[wn_name][RefPath.PODS][pod_name] = new_pod

        if remaining_methods:
            print("create a new container and add the methods in it")
            container_name = "c" + str(len(remaining_containers[1:]) + 1)
            new_container = {
                "name": container_name,
                "metrics": {
                    "load": ""
                }
            }

            ref_path = RefPath(cluster.name, new_worker_node["name"], pod_name, container_name)
            cluster_template[wn_name][RefPath.PODS][pod_name][RefPath.CONTAINERS][container_name] = new_container

            # changing the RefPath of remaining methods
            for r_method in remaining_methods:
                method = copied_template[RefPath.PATHS][r_method.path_name][r_method.method_name]
                method[RefPath.X_LOCATION][RefPath.REF] = ref_path.full_path


def monitor_pods(container_groups, methods, copied_template):
    delete_able_containers = set()
    # scaling based upon the pods
    for group in container_groups:
        print("entered in monitoring the container groups.")

        #         segmenting the containers before and after the threshold
        joined_containers, remaining_containers = _join_components(MAX_POD_LOAD, group.get_contributed_components())

        first_remaining_container = remaining_containers[0]
        first_remaining_container_methods = []

        for method in methods:
            if method.ref_path.full_path == first_remaining_container.ref_path:
                first_remaining_container_methods.append(method)
        sum_of_method_loads = sum(m.load for m in first_remaining_container_methods)

        # creating a new instance of MethodGroup for remaining container & its methods
        method_group = MethodGroup(first_remaining_container.load, sum_of_method_loads,
                                   first_remaining_container_methods)
        sum_of_joined_containers_contribution = sum(j_c.contribution for j_c in joined_containers)

        joined_methods, remaining_methods = _join_components(
            MAX_POD_LOAD - sum_of_joined_containers_contribution,
            method_group.get_contributed_components())

        current_ref_path = RefPath(group.components[0].ref_path)
        pod_name = "pod" + str(len(current_ref_path.worker_node) + 1)
        new_pod = {
            "name": pod_name,
            "metrics": {
                "load": ""
            }, "containers": {}
        }

        container_name = "c" + str(len(remaining_containers[1:]) + 1)
        new_container = {
            "name": container_name,
            "metrics": {
                "load": ""
            }
        }
        remaining_containers.append(new_container)

        worker_nodes = copied_template[RefPath.INFO][RefPath.X_CLUSTERS][current_ref_path.cluster][
            RefPath.WORKER_NODES]

        method_path = copy.deepcopy(current_ref_path)
        method_path.pod_name = pod_name
        method_path.container_name = container_name

        for r_method in remaining_methods:
            print(r_method)
            method = copied_template[RefPath.PATHS][r_method.path_name][r_method.name]
            method[RefPath.X_LOCATION][RefPath.REF] = method_path.full_path
        for r_container in remaining_containers:
            new_pod["containers"][container_name] = r_container

            # deleting the existing container which will be added to new pod later
            print("came once")
            delete_able_containers.add(
                RefPath(current_ref_path.cluster, current_ref_path.worker_node, current_ref_path.pod_name,
                        r_container.container_name))

        print(delete_able_containers)

        worker_nodes[current_ref_path.worker_node][RefPath.PODS][pod_name] = new_pod
