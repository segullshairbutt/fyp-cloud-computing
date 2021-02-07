import copy
import json
import logging
import os

import monitoring_app.data_generator as data_generator
import monitoring_app.templates.config_templates as config_templates
from deployment_generator import utilities
from monitoring_app.constants import MAX_WN_LOAD, MAX_POD_LOAD, DEFAULT_SCHEMA_NAME, CL_LEVEL, WN_LEVEL, POD_LEVEL, \
    SCHEMA_LEVEL, MIN_WN_LOAD, MIN_POD_LOAD
from monitoring_app.models import Cluster, ContainerGroup, MethodGroup, PodGroup, RefPath, Method, Container
from monitoring_app.utilities import _join_components, _gen_dict_extract, _get_schema_only, clean_template, \
    reorder_template

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

        cluster = data_file_content[RefPath.X_CLUSTERS][next(iter(data_file_content[RefPath.X_CLUSTERS]))]
        cl_load = cluster["metrics"]["load"]

        worker_node = cluster[RefPath.WORKER_NODES][next(iter(cluster[RefPath.WORKER_NODES]))]
        wn_load = worker_node['metrics']['load']

        pod = worker_node[RefPath.PODS][next(iter(worker_node[RefPath.PODS]))]
        pod_load = pod['metrics']['load']

        container = pod[RefPath.CONTAINERS][next(iter(pod[RefPath.CONTAINERS]))]
        container_load = container['metrics']['load']

        first_path_key = next(iter(data_file_content[RefPath.PATHS]))
        first_method_key = next(iter(data_file_content[RefPath.PATHS][first_path_key]))

        method_load = data_file_content[RefPath.PATHS][first_path_key][first_method_key]["x-metrics"]["load"]

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
        for path_name, path in initial_template[RefPath.PATHS].items():
            for method_name, method in path.items():
                ref_path = RefPath(method[RefPath.X_LOCATION][RefPath.REF])

                all_references = list(set(_gen_dict_extract(RefPath.REF, method)))
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
                copied_template[RefPath.INFO][RefPath.X_CLUSTERS][ref_path.cluster][RefPath.WORKER_NODES][
                    ref_path.worker_node][RefPath.PODS][ref_path.pod_name][RefPath.CONTAINERS][
                    new_container] = container_template

                for method in schema_methods:
                    method.ref_path.container_name = new_container
                    method.full_method[RefPath.X_LOCATION][RefPath.REF] = method.ref_path.full_path
                    copied_template[RefPath.PATHS][method.path_name][method.method_name] = method.full_method
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
        utilities.create_server_stubs(os.path.join(project.config_data_path, configfile),project.directory)

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
            print('--------------------------')

            # creating name for new configuration file
            new_config_file = str(_get_new_filetag(config_dir_path)) + 'config.json'

            # creating name for new data file
            new_data_file = str(_get_new_filetag(config_dir_path)) + 'data.json'

            # creating config.json file with new template
            _write_config_file(new_template, config_dir_path, new_config_file)

            # creating the data.json file populate data according to new template
            data_generator.generate_data(config_dir_path, new_config_file, new_data_file)

            # creating the server side code
            utilities.create_server_stubs(
                os.path.join(project.config_data_path, new_config_file), project.directory)

            """create docker files according to how many containers we need in new config
            we are passing prev_files_tags here because at last 2 function that we call above
            already created new files"""

            # generate_deployment_files(config_and_metrics_generator.get_latest_filetag(config_dir_path), paths)


def _monitor_scaling(config_data, config_path):
    VERBOSE_LOGGER.info("Monitor the scaling of pods and containers.")

    file_name = str(_get_latest_filetag(config_path)) + "config.json"
    template = copy.deepcopy(_get_config_file(os.path.join(config_path, file_name)))
    copied_template = copy.deepcopy(template)

    for single_data_object in config_data:
        # converting provided data to objects
        clusters, methods = _derive_components(single_data_object)

        scalable_wns, scalable_pods = _get_scalable_components(clusters, methods)

        # monitoring based on pods
        _monitor_pods(_get_container_groups(scalable_pods), methods, copied_template)
        # scaling based upon the worker-nodes
        _monitor_worker_nodes(_get_pod_groups(scalable_wns), methods, clusters[0], copied_template)

        if copied_template == template:
            LOGGER.info("No changed detected in template.")
            print("no changes detected to template.")
        else:
            _adjust_schema_levels(copied_template)
            # cleaning template
            LOGGER.info("Cleaning template to remove all not-required components.")
            clean_template(copied_template)
            # reordering the template which is out of order now
            LOGGER.info("Reordering the template.")
            reorder_template(copied_template)

            LOGGER.info("Returning new template. ")
            return copied_template

    # if no new template is made None type is returned back
    return None


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


def _adjust_schema_levels(template):
    VERBOSE_LOGGER.info("Adjusting the storage level of schemas.")

    config_paths = template[RefPath.PATHS]
    methods = []
    for path_name, path in config_paths.items():
        for method_name, method in path.items():
            ref_path = RefPath(method[RefPath.X_LOCATION][RefPath.REF])

            all_references = list(set(_gen_dict_extract(RefPath.REF, method)))
            schema_name = _get_schema_only(all_references)

            methods.append(Method(path_name, method_name, ref_path, method["x-metrics"]["load"], schema_name, method))

    method_schemas = {}
    for method in methods:
        method_schemas.setdefault(method.schema_name, {RefPath.PODS: set(), RefPath.WORKER_NODES: set()})
        method_schemas[method.schema_name][RefPath.PODS].add(method.ref_path.pod_name)
        method_schemas[method.schema_name][RefPath.WORKER_NODES].add(method.ref_path.worker_node)

    # it will remove the schema of stateless methods
    if DEFAULT_SCHEMA_NAME in method_schemas.keys():
        del method_schemas[DEFAULT_SCHEMA_NAME]

    final_schema_levels = dict()
    for schema_name, values in method_schemas.items():
        if len(values["worker-nodes"]) > 1:
            LOGGER.info(f"Set storage-level of {schema_name} to {CL_LEVEL}")
            final_schema_levels[schema_name] = CL_LEVEL
        elif len(values["pods"]) > 1:
            LOGGER.info(f"Set storage-level of {schema_name} to {WN_LEVEL}")
            final_schema_levels[schema_name] = WN_LEVEL
        else:
            LOGGER.info(f"Set storage-level of {schema_name} to {POD_LEVEL}")
            final_schema_levels[schema_name] = POD_LEVEL

    config_schemas = template["components"]["schemas"]
    for schema_name, level in final_schema_levels.items():
        if schema_name in config_schemas.keys():
            config_schemas[schema_name][SCHEMA_LEVEL] = level


def _get_wn(wn_name):
    return {
        "name": wn_name,
        "metrics": {"load": ""},
        "pods": {}
    }


def _get_pod(pod_name):
    return {
        "name": pod_name,
        "metrics": {
            "load": ""
        }, "containers": {}
    }


def _get_container(container_name):
    return {
        "id": container_name,
        "metrics": {
            "load": ""
        }
    }


def _derive_components(single_data_obj):
    clusters = []
    cls = single_data_obj[RefPath.X_CLUSTERS]

    for cl in cls.values():
        ref_path = RefPath.INITIAL + cl["name"]
        clusters.append(Cluster(cl["name"], cl["metrics"]["load"], cl, ref_path))

    methods = []
    data_paths = single_data_obj[RefPath.PATHS]
    for path_name, path in data_paths.items():
        for method_name, method in path.items():
            ref_path = RefPath(method[RefPath.X_LOCATION][RefPath.REF])

            all_references = list(set(_gen_dict_extract('$ref', method)))
            schema_name = _get_schema_only(all_references)

            methods.append(
                Method(path_name, method_name, ref_path, method["x-metrics"]["load"], schema_name, method))
    return clusters, methods


def _get_scalable_components(clusters, methods):
    scalable_wns = []
    scalable_pods = []
    for cluster in clusters:
        _adjust_and_merge_wns(cluster.worker_nodes, methods, cluster.full_component[RefPath.WORKER_NODES])

        for worker_node in cluster.worker_nodes:
            if worker_node.load < MAX_WN_LOAD:
                print("no need to scale ", str(worker_node))

                _adjust_and_merge_pods(worker_node.pods, methods, worker_node.full_component[RefPath.PODS])
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


def _adjust_and_merge_pods(scalable_pods, methods, all_pods):
    min_load_pods = []

    #     if there is only one pod it will return as it is
    if len(scalable_pods) < 2:
        LOGGER.info("Number of pods is less than 2.")
        return scalable_pods

    #     creating a new list so that we can modify the original one
    for pod in list(scalable_pods):
        if pod.load <= MIN_POD_LOAD:
            min_load_pods.append(pod)
            scalable_pods.remove(pod)
            all_pods.pop(pod.name)

    LOGGER.info("Replacing Pod from RefPath of methods.")
    first_pod = scalable_pods[0]
    for pod in min_load_pods:
        first_pod.full_component['metrics']['load'] += pod.load

        for container in pod.containers:

            container_methods = filter(lambda method: method.ref_path.full_path == container.ref_path, methods)
            first_pod_containers = first_pod.full_component[RefPath.CONTAINERS]
            new_container_name = "c" + str(len(first_pod_containers) + 1)
            first_pod_containers[new_container_name] = container.full_component

            # don't forget to chage the id of container
            first_pod_containers[new_container_name]['id'] = new_container_name

            for container_method in container_methods:
                print("Changed from:", container_method.ref_path.full_path)

                # getting ref_path of first container in first selected pod

                container_method.ref_path = RefPath(first_pod.containers[0].ref_path)
                container_method.ref_path.container_name = new_container_name

                print("To:", container_method.ref_path.full_path)


def _adjust_and_merge_wns(wns, methods, all_nodes):
    min_load_wns = []

    # If there is only one worker-node it will return as it is
    if len(wns) < 2:
        LOGGER.info("Worker-nodes are less than 2.")
        return wns

    # Creating a new list so that we can modify the original one
    for wn in list(wns):
        if wn.load <= MIN_WN_LOAD:
            min_load_wns.append(wn)
            wns.remove(wn)
            all_nodes.pop(wn.name)

    LOGGER.info("Replacing Worker-Node from RefPath of methods.")
    first_wn = wns[0]
    for wn in min_load_wns:
        first_wn.full_component['metrics']['load'] += wn.load

        for pod in wn.pods:
            first_wn_pods = first_wn.full_component[RefPath.PODS]
            new_pod_name = "pod" + str((len(first_wn_pods) + 1))
            first_wn_pods[new_pod_name] = pod.full_component
            first_wn_pods[new_pod_name]['id'] = new_pod_name

            for container in pod.containers:
                filtered_methods = filter(lambda m: m.ref_path.full_path == container.ref_path, methods)

                for method in filtered_methods:
                    print("Changed from:", method.ref_path.full_path)
                    method.ref_path.pod_name = new_pod_name
                    method.ref_path.worker_node = first_wn.name
                    print("To:", method.ref_path.full_path)


def _monitor_worker_nodes(pod_groups, methods, cluster, copied_template):
    VERBOSE_LOGGER.info("Entered into _monitor_worker_nodes")
    for group in pod_groups:
        LOGGER.info("Iterating into pod groups.")
        cluster_template = copied_template[RefPath.INFO][RefPath.X_CLUSTERS][cluster.name][RefPath.WORKER_NODES]
        joined_pods, remaining_pods = _join_components(MAX_WN_LOAD, group.get_contributed_components())

        if not remaining_pods:
            LOGGER.info("No remaining pods found.")
        else:
            # getting first pod from remaining pods
            first_remaining_pod = remaining_pods[0]
            sum_of_container_loads = sum(c.load for c in first_remaining_pod.containers)
            container_group = ContainerGroup(first_remaining_pod.load, sum_of_container_loads,
                                             first_remaining_pod.containers)

            sum_of_joined_pods_contribution = sum(j_p.contribution for j_p in joined_pods)
            joined_containers, remaining_containers = _join_components(
                (MAX_WN_LOAD - sum_of_joined_pods_contribution), container_group.get_contributed_components())

            print("Joined Containers: " + str(len(joined_containers)),
                  "Remaining Containers: " + str(len(remaining_containers)))

            wn_name = "wn" + str(len(cluster.worker_nodes) + 1)
            LOGGER.info("Creating a new worker-node: " + wn_name)
            new_worker_node = _get_wn(wn_name)

            pod_name = "pod" + str(len(remaining_pods[1:]) + 1)
            LOGGER.info("Creating a new pod: " + pod_name)
            new_pod = _get_pod(pod_name)
            joined_methods = []

            if not remaining_containers:
                LOGGER.info("No Remaining containers found.")
            else:
                # getting first container from remaining containers
                first_remaining_container = remaining_containers[0]

                first_remaining_container_methods = []
                for method in methods:
                    if method.ref_path.full_path == first_remaining_container.ref_path:
                        first_remaining_container_methods.append(method)
                sum_of_method_loads = sum(m.load for m in first_remaining_container_methods)
                method_group = MethodGroup(first_remaining_container.load, sum_of_method_loads,
                                           first_remaining_container_methods)
                sum_of_joined_containers_contribution = sum(j_c.contribution for j_c in joined_containers)
                joined_methods, remaining_methods = _join_components(
                    MAX_WN_LOAD - sum_of_joined_pods_contribution - sum_of_joined_containers_contribution,
                    method_group.get_contributed_components())

                if remaining_methods:
                    LOGGER.info("Remaining methods exist, so create a new container and add them.")
                    container_name = "c" + str(len(remaining_containers[1:]) + 1)
                    new_container_ref_path = RefPath(cluster.name, new_worker_node["name"], pod_name, container_name)
                    new_pod[RefPath.CONTAINERS][container_name] = _get_container(container_name)
                    # have to be seen later here.
                    # changing the RefPath of remaining methods
                    for r_method in remaining_methods:
                        method = copied_template[RefPath.PATHS][r_method.path_name][r_method.method_name]
                        method[RefPath.X_LOCATION][RefPath.REF] = new_container_ref_path.full_path

            remaining_containers_to_deploy = remaining_containers if len(joined_methods) == 0 else remaining_containers[
                                                                                                   1:]
            if remaining_containers_to_deploy:
                LOGGER.info("Remaining containers exist, so create a new pod and add them. ")
                print("create a new pod and add the containers in it.")
                for r_container in remaining_containers_to_deploy:
                    r_container_ref_path = RefPath(r_container.ref_path)
                    r_container_ref_path.pod_name = pod_name
                    r_container_ref_path.worker_node = wn_name

                    new_pod[RefPath.CONTAINERS][r_container.name] = _get_container(r_container.name)
                    # replacing the path of methods
                    for method in methods:
                        if method.ref_path.full_path == r_container.ref_path:
                            LOGGER.info("Scaling the methods of " + str(r_container))
                            method.ref_path = r_container_ref_path
                            ind_method = copied_template[RefPath.PATHS][method.path_name][method.method_name]
                            ind_method[RefPath.X_LOCATION][RefPath.REF] = r_container_ref_path.full_path
                            print(method)

            # it means that all containers in first pod needs to get in new WN
            remaining_pods_to_deploy = remaining_pods if len(joined_containers) == 0 else remaining_pods[1:]
            if remaining_pods_to_deploy:
                LOGGER.info("Add the pods into newly created WN.")
                for r_pod in remaining_pods_to_deploy:
                    new_worker_node[RefPath.PODS][r_pod.name] = r_pod.full_component
                    for r_container in r_pod.containers:
                        r_container_ref_path = RefPath(r_container.ref_path)
                        r_container_ref_path.worker_node = wn_name

                        for method in methods:
                            if method.ref_path.full_path == r_container.ref_path:
                                LOGGER.info("scaling ", method)
                                method.ref_path = r_container_ref_path
                                ind_method = copied_template[RefPath.PATHS][method.path_name][method.method_name]
                                ind_method[RefPath.X_LOCATION][RefPath.REF] = r_container_ref_path.full_path

            # adding a new pod only if it has containers
            if new_pod[RefPath.CONTAINERS]:
                new_worker_node[RefPath.PODS][new_pod["name"]] = new_pod
            else:
                LOGGER.info("No containers found in new POD, so it is ignored.")

            # adding the newly created worker node
            if new_worker_node[RefPath.PODS]:
                cluster_template[wn_name] = new_worker_node
            else:
                LOGGER.info("No PODS found in new worker-node, so it is ignored.")


def _monitor_pods(container_groups, methods, copied_template):
    VERBOSE_LOGGER.info("entered in _monitor_pods")
    # scaling based upon the pods
    for group in container_groups:
        LOGGER.info("iterating the container_groups")

        # segmenting the containers before and after the threshold
        joined_containers, remaining_containers = _join_components(MAX_POD_LOAD, group.get_contributed_components())

        current_ref_path = RefPath(group.components[0].ref_path)
        config_pods = copied_template[RefPath.INFO][RefPath.X_CLUSTERS][current_ref_path.cluster][
            RefPath.WORKER_NODES][current_ref_path.worker_node][RefPath.PODS]

        pod_name = "pod" + str(len(config_pods) + 1)
        new_pod = _get_pod(pod_name)
        LOGGER.info("New pod name: " + pod_name)

        if not remaining_containers:
            LOGGER.info("No remaining containers found.")
        else:
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

            LOGGER.info("Joined methods: " + str(len(joined_methods)))
            LOGGER.info("Remaining methods: " + str(len(remaining_methods)))

            container_name = "c" + str(len(remaining_containers[1:]) + 1)
            new_container = _get_container(container_name)
            LOGGER.info("New Container name: " + container_name)

            method_path = copy.deepcopy(current_ref_path)
            method_path.pod_name = pod_name
            method_path.container_name = container_name
            remaining_containers.append(Container(container_name, 0, new_container, method_path.full_path, True))

            for r_method in remaining_methods:
                print(r_method)
                method = copied_template[RefPath.PATHS][r_method.path_name][r_method.method_name]
                method[RefPath.X_LOCATION][RefPath.REF] = method_path.full_path
                LOGGER.info("Remaining methods added into new container: " + method_path.container_name)

            current_container_counter = len(remaining_containers[1:])
            for r_container in remaining_containers:
                if r_container.is_new:
                    # it means that this container is new container and is to be added as it is.
                    new_pod["containers"][r_container.name] = r_container.full_component
                else:
                    current_container_counter += 1
                    # continuously incrementing the number of containers
                    container_name = "c" + str(current_container_counter)
                    r_container.full_component["id"] = container_name
                    new_pod["containers"][container_name] = r_container.full_component

                LOGGER.info("Remaining containers are inserted into new Pod: " + new_pod["name"])

            config_pods[pod_name] = new_pod
