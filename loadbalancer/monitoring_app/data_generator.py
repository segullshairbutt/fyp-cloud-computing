import copy
import random
import os
import json


def get_random_load(min_range, max_range):
    return random.randrange(min_range, max_range)


def generate_data(dir_path, config_file, data_file, **kwargs):
    # min and max load range for pod metrics
    pod_min_cpu = 1
    pod_max_cpu = 100
    pod_min_ram = 1
    pod_max_ram = 100

    pod_ram_load = 0
    pod_cpu_load = 0
    container_load = 0
    endpoint_load = 0

    # min and max range for container metrics (load)
    container_min_range = 1
    container_max_range = 95

    # min and max range for container's services
    service_max_range = 95
    service_min_range = 1
    if kwargs:
        if 10 < kwargs['pod_cpu'] < 85:
            pod_min_cpu = kwargs['pod_cpu'] - 10
            pod_max_cpu = kwargs['pod_cpu'] + 10
        if 10 < kwargs['pod_ram'] < 85:
            pod_min_ram = kwargs['pod_ram'] - 10
            pod_max_ram = kwargs['pod_ram'] + 10
        if 10 < kwargs['container_load'] < 85:
            container_min_range = kwargs['container_load'] - 10
            container_max_range = kwargs['container_load'] + 10
        if 10 < kwargs['method_load'] < 85:
            service_min_range = kwargs['method_load'] - 10
            service_max_range = kwargs['method_load'] + 10

    # getting the path of the latest config file
    path_config = os.path.join(dir_path, config_file)

    # reading the latest config file
    with open(path_config, 'r', encoding='utf-8') as f:
        data = f.read()
        dataset = json.loads(data)
    new_data = []

    # set the default load value that can use only for first object in any dataset

    # iterate loop 10 times to generate 10 objects of dataset
    for load in range(3):
        config = copy.deepcopy(dataset)

        pods = config["info"]["x-pods"]
        for pod in pods.values():
            container_counter = 0
            # get the random value for pod_cpu load
            pod_cpu_load = get_random_load(pod_min_cpu, pod_max_cpu)
            # get the random value for pod_ram load
            pod_ram_load = get_random_load(pod_min_ram, pod_max_ram)

            # setting the pod metrics(cpu and ram)
            pod['metrics']['CPU'] = pod_cpu_load
            pod['metrics']['RAM'] = pod_ram_load

            for container in pod['containers'].values():
                # generating the new container name
                container_counter = container_counter + 1
                # getting the load of container
                container_load = get_random_load(container_min_range, container_max_range)
                container['metrics']['load'] = container_load

        paths = config["paths"]
        for path in paths.values():
            for method in path.values():
                endpoint_load = get_random_load(service_min_range, service_max_range)
                method["x-metrics"]["load"] = endpoint_load
        new_object = {
            "x-pods": pods,
            "paths": paths
        }
        new_data.append(new_object)

        # confusing here need to understand it what's going on here.
        # updating the min and max range of pod(cpu and ram) for next iteration
        if 90 > pod_cpu_load > 10:
            pod_min_cpu = pod_cpu_load - 10
            pod_max_cpu = pod_cpu_load + 10
        if 90 > pod_ram_load > 10:
            pod_min_ram = pod_ram_load - 10
            pod_max_ram = pod_ram_load + 10
        # ************************************************
        # update the container load (min and max range)
        if 85 > container_load > 10:
            container_min_range = container_load - 10
            container_max_range = container_load + 10

        if 10 < endpoint_load < 85:
            service_min_range = endpoint_load - 10
            service_max_range = endpoint_load + 10

    path_data = os.path.join(dir_path, data_file)
    with open(path_data, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
