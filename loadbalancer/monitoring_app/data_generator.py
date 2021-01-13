import copy
import random
import os
import json


def get_random_load(min_range, max_range):
    return random.randrange(min_range, max_range)


def generate_data(dir_path, config_file, data_file, **kwargs):
    cl_min_range = 1
    cl_max_range = 90

    wn_min_range = 1
    wn_max_range = 90

    pod_min_range = 1
    pod_max_range = 95

    container_min_range = 1
    container_max_range = 95

    method_min_range = 10
    method_max_range = 95

    cl_load = 0
    wn_load = 0
    pod_load = 0
    container_load = 0
    method_load = 0

    if kwargs:
        if 10 < kwargs['cl_load'] < 85:
            cl_min_range = kwargs['cl_load'] - 10
            cl_max_range = kwargs['cl_load'] + 10
        if 10 < kwargs['wn_load'] < 85:
            wn_min_range = kwargs['wn_load'] - 10
            wn_max_range = kwargs['wn_load'] + 10
        if 10 < kwargs['pod_load'] < 85:
            pod_min_range = kwargs['pod_load'] - 10
            pod_max_range = kwargs['pod_load'] + 10
        if 10 < kwargs['container_load'] < 85:
            container_min_range = kwargs['container_load'] - 10
            container_max_range = kwargs['container_load'] + 10
        if 10 < kwargs['method_load'] < 85:
            method_min_range = kwargs['method_load'] - 10
            method_max_range = kwargs['method_load'] + 10

    # getting the path of the latest config file
    path_config = os.path.join(dir_path, config_file)

    # reading the latest config file
    with open(path_config, 'r', encoding='utf-8') as f:
        data = f.read()
        template_config = json.loads(data)
    new_data = []

    for load in range(3):
        config = copy.deepcopy(template_config)
        clusters = template_config["info"]["x-clusters"]

        for cluster in clusters.values():
            cl_load = cluster["metrics"]["load"] = get_random_load(cl_min_range, cl_max_range)

            for wn in cluster["worker-nodes"].values():
                wn_load = wn["metrics"]["load"] = get_random_load(wn_min_range, wn_max_range)

                for pod in wn["pods"].values():
                    pod_load = pod['metrics']['load'] = get_random_load(pod_min_range, pod_max_range)

                    for container in pod['containers'].values():
                        container_load = container['metrics']['load'] = get_random_load(container_min_range,
                                                                                        container_max_range)

        paths = config["paths"]
        for path in paths.values():
            for method in path.values():
                method_load = method["x-metrics"]["load"] = get_random_load(method_min_range, method_max_range)

        new_object = {
            "x-clusters": clusters,
            "paths": paths
        }
        new_data.append(new_object)

        # ************************************************
        # update the container load (min and max range)
        if 10 < cl_load < 85:
            cl_min_range = cl_load - 10
            cl_max_range = cl_load + 10

        if 10 < wn_load < 85:
            wn_min_range = wn_load - 10
            wn_max_range = wn_load + 10

        if 10 < pod_load < 85:
            pod_min_range = pod_load - 10
            pod_max_range = pod_load + 10

        if 10 < container_load < 85:
            container_min_range = container_load - 10
            container_max_range = container_load + 10

        if 10 < method_load < 85:
            method_min_range = method_load - 10
            method_max_range = method_load + 10

    path_data = os.path.join(dir_path, data_file)
    with open(path_data, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
