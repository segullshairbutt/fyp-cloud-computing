import copy
import json
import logging
import os
import random

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def get_config_file(filepath):
    VERBOSE_LOGGER.info("getting config file.")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read()
        dataset = json.loads(data)
    return dataset


def write_config_file(template, dir_path, filename):
    VERBOSE_LOGGER.info("generating config file.")
    print('filename is ', filename)
    path = os.path.join(dir_path, filename)
    print('writing config file../.')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)


DIR = os.getcwd()
DIR = os.path.join(DIR, 'docker/dataGenerationAndMonitoring/Iterations')


def get_total_files_length(dir_path):
    dir_size = (len(os.listdir(dir_path)))
    # as it contains config and data files
    total_files = int(dir_size / 2)

    return total_files


def get_new_filetag(dir_path):
    """This method will return integer that is the number for new next file
     in that directory"""

    dir_size = (len(os.listdir(dir_path)))
    dir_size = int(dir_size / 2)
    new_file_tag = dir_size + 1
    if new_file_tag < 10:
        new_file_tag = str("0" + str(new_file_tag))
    return new_file_tag


def get_latest_filetag(dir_path):
    """get the number of latest configuration file"""

    dir_size = (len(os.listdir(dir_path)))
    prev_file_tag = int(dir_size / 2)
    if prev_file_tag < 10:
        prev_file_tag = str("0" + str(prev_file_tag))
    return prev_file_tag


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
        if 10 < kwargs['service_load'] < 85:
            service_min_range = kwargs['service_load'] - 10
            service_max_range = kwargs['service_load'] + 10

    # getting the path of the latest config file
    path_config = os.path.join(dir_path, config_file)

    # reading the latest config file
    with open(path_config, 'r', encoding='utf-8') as f:
        data = f.read()
        dataset = json.loads(data)
    new_data = []

    # set the default load value that can use only for first object in any dataset

    # iterate loop 10 times to generate 10 objects of dataset
    for load in range(1):
        config = copy.deepcopy(dataset)

        for pod_obj in config:
            for pod in pod_obj.values():
                # make container_counter to 0 on every new pod so we can calculate the total no of container on each pod
                container_counter = 0

                # get the random value for pod_cpu load
                pod_cpu_load = get_random_load(pod_min_cpu, pod_max_cpu)
                # get the random value for pod_ram load
                pod_ram_load = get_random_load(pod_min_ram, pod_max_ram)

                # setting the pod metrics(cpu and ram)
                pod['metrics']['CPU'] = pod_cpu_load
                pod['metrics']['RAM'] = pod_ram_load

                for container in pod['containers']:

                    # generating the new container name
                    container_counter = container_counter + 1
                    # getting the load of container
                    container_load = get_random_load(container_min_range, container_max_range)
                    container['metrics']['load'] = container_load

                    for service in container['services']:
                        # getting the first element of service dict e-g 'paths':{}
                        api_path = service["paths"]
                        # getting path_name which is first_element e-g 'paths':{'pets':{}}
                        api_methods = api_path[next(iter(api_path))]

                        for method in api_methods.values():
                            endpoint_load = get_random_load(service_min_range, service_max_range)
                            method["metrics"]["load"] = endpoint_load

                        # for metrics in service['metrics']:
                        #     metrics['load'] = service_load
            new_data.append(pod_obj)

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
