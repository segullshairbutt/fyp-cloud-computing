import copy
import logging
import os
import random

from . import config_and_metrics_generator
from .config_and_metrics_generator import get_latest_filetag, get_config_file

verbose_logger = logging.getLogger("mid-verbose")
logger = logging.getLogger("root")

MAX_ENDPOINT_LOAD = 60
MAX_CPU_USAGE = 75
MAX_RAM_USAGE = 70

MIN_ENDPOINT_LOAD = 25
MIN_CPU_USAGE = 40
MIN_RAM_USAGE = 40


def monitor_scaling(pods, config_path):
    verbose_logger.info("Monitor the scaling of pods and containers.")

    file_name = get_latest_filetag(config_path) + "config.json"
    previous_template = copy.deepcopy(get_config_file(os.path.join(config_path, file_name)))
    template = copy.deepcopy(get_config_file(os.path.join(config_path, file_name)))
    for pod_obj in pods:
        for pod in pod_obj.values():
            cpu_usage = pod["metrics"]["CPU"]
            ram_usage = pod["metrics"]["RAM"]

            # if cpu and ram usage is within normal threshold it will return the same template
            if MIN_CPU_USAGE < cpu_usage < MAX_CPU_USAGE and MIN_RAM_USAGE < ram_usage < MAX_RAM_USAGE:
                print(str(cpu_usage) + "--> (" + str(MIN_CPU_USAGE) + ", " + str(MAX_CPU_USAGE) + ")")
                print(str(ram_usage) + "--> (" + str(MIN_RAM_USAGE) + ", " + str(MAX_RAM_USAGE) + ")")
                logger.info(f"no changes required for [{pod['name']}]")
                continue
            else:
                for container in pod["containers"]:
                    for service in container["services"]:
                        api_path = service["paths"]
                        # getting first element e-g paths{'pets': {}}
                        path_name = next(iter(api_path))

                        api_methods = api_path[path_name]
                        # it is getting the number of pods from current template
                        pod_number = len(template[0].items())

                        for api_method_name, api_method_body in api_methods.items():
                            load = api_method_body["metrics"]["load"]
                            # this case if maximum threshold of an endpoint is reached
                            if load > MAX_ENDPOINT_LOAD:

                                # random_number = random.randint(pod_number + 1, pod_number + 3)
                                # as it is going to create a new pod
                                pod_number = pod_number + 1
                                print("Scaling up--------")
                                new_port = int(service["port"]) + pod_number
                                print(service["port"], path_name + ":" + api_method_name + "->>" + str(new_port) + ":"
                                      + str(pod_number))

                                new_pod = _create_new_pod(str(pod_number), new_port, copy.deepcopy(api_method_body),
                                                          api_method_name, path_name)
                                print("load --> ", str(load))
                                template[0][new_pod["name"]] = new_pod

                                # delete api_methods from existing template
                                _delete_api_method(template, service["port"], path_name, api_method_name)
                                # _clean_template(template)

                            elif load <= MIN_ENDPOINT_LOAD:
                                print("Scaling Down------")
                                print("load --> ", str(load))

                                mergeable_port = _find_port_to_merge(pod, load, service["port"])
                                print(service["port"], path_name + ":" + api_method_name + "<->" + str(mergeable_port))

                                if mergeable_port == service["port"]:
                                    # it means that no port is capable to take the load
                                    continue
                                endpoint = _create_endpoint(path_name, api_method_name, api_method_body)
                                _merge_template(template, endpoint, mergeable_port)

                                # delete api_methods from existing template
                                _delete_api_method(template, service["port"], path_name, api_method_name)

            if template == previous_template:
                continue
            else:
                _clean_template(template)
                return template
    return None


def _create_new_pod(template_no, port, api, method_name, path_name):
    api["metrics"]["load"] = ""
    new_pod = {
        "name": "pod" + template_no,
        "metrics": {
            "CPU": "",
            "RAM": ""
        },
        "containers": [
            {
                "id": "c1",
                "metrics": {
                    "load": ""
                },
                "services": [
                    {
                        "port": port,
                        "paths": _create_endpoint(path_name, method_name, api)
                    }
                ]
            }
        ]
    }
    return new_pod


def _create_endpoint(path_name, method_name, api):
    api["metrics"]["load"] = ""
    return {
        path_name: {
            method_name: api
        }
    }


def _delete_api_method(pods, port, path_name, method_name):
    for pod_obj in pods:
        for pod in pod_obj.values():
            containers = pod["containers"]
            for container in containers:
                services = container["services"]
                for service in services:
                    if service["port"] != port:
                        continue

                    api_path = service["paths"]
                    api_path_name = next(iter(api_path))

                    if api_path_name != path_name:
                        continue

                    api_methods = api_path[api_path_name]

                    for api_method_name in list(api_methods.keys()):
                        if api_method_name == method_name:
                            del api_methods[api_method_name]


def _find_port_to_merge(pod, new_endpoint_load, current_port):
    logger.info("new_endpoint_load: " + str(new_endpoint_load))
    # if no port is capable of getting the load, previous port will be used
    port = current_port

    for container in pod["containers"]:
        for service in container["services"]:
            service_paths = service["paths"]

            calculated_load = _get_post_load_of_endpoint(service_paths, new_endpoint_load)
            # we don't want to make execution for current port.
            if current_port == service["port"]:
                continue

            if calculated_load >= MAX_ENDPOINT_LOAD:
                print("You can't merge at")
                print(f"port ${service['port']}")
                continue
            else:
                print("You can merge at")
                print(f"port ${service['port']}")
                port = service["port"]
                break
    return port


def _get_post_load_of_endpoint(api_paths, new_load):
    service_counter = 0
    api_load = new_load

    # if any load is provided it means that you already have a new endpoint
    # if api_load > 0:
    #     service_counter = 1

    for api_path in api_paths.values():
        for api_method in api_path.values():
            method_load = api_method["metrics"]["load"]

            # if there isn't any load at any method it will continue
            service_counter += 1
            if type(method_load) != int:
                continue
            api_load += int(method_load)

    return api_load / service_counter


def _merge_template(template, endpoint, port):
    for pod_obj in template:
        for pod in pod_obj.values():

            for container in pod["containers"]:
                for service in container["services"]:
                    if service["port"] != port:
                        logger.info("port not matched.")
                        continue
                    else:
                        api_paths = service["paths"]
                        path_name = next(iter(endpoint))
                        method_name = next(iter(endpoint[path_name]))
                        # we are trying to get previous available same key for path
                        api_method = api_paths.setdefault(path_name, {method_name: {}})
                        api_method[method_name] = endpoint[path_name][method_name]
                        logger.info("endpoint merged at port: " + str(service["port"]))

                        return


def _delete_extra_services(services):
    temp_service = []

    if len(services):
        while services:
            service = services.pop()
            paths = service["paths"]
            # verifying that the path length exists
            if len(paths):
                api_methods = paths[next(iter(paths))]
                if len(api_methods):
                    temp_service.append(service)

        while temp_service:
            services.append(temp_service.pop())


def _delete_extra_paths(services):
    temp_service = []

    if len(services):
        while services:
            service = services.pop()

            paths = service["paths"]
            # delete extra paths here.
            new_paths = {k: v for k, v in paths.items() if len(v)}
            service["paths"] = new_paths
            temp_service.append(service)

        while temp_service:
            services.append(temp_service.pop())


def _clean_template(template):
    for pod_obj in template:
        for pod_name in list(pod_obj.keys()):
            pod = pod_obj[pod_name]

            for container in pod["containers"]:
                _delete_extra_services(container["services"])

            # if there are no services/endpoints in a pod container and there is only one container
            if len(pod["containers"]) == 1 and not len(pod["containers"][0]["services"]):
                del pod_obj[pod["name"]]


def monitor_data(dataset, config_path):
    """Monitor the metrics of pods , container and services"""
    verbose_logger.info("Monitoring the metrics of pods containers and services.")
    return False
    for data in dataset:
        counter_container = 0
        scale_up_services_counter = 0
        scale_down_services_counter = 0
        scale_down_counter_container = 0

        down_prev_port = []
        down_curr_port = []
        new_port = []
        curr_port = []

        # getting the value of pod metrics and save in cpu and ram variable
        cpu = data['pod']['metrics']['CPU']
        ram = data['pod']['metrics']['RAM']

        # copy the current configuration template in variable (template)
        template = copy.deepcopy(config_and_metrics_generator.get_config_file(config_path))

        # scaling down
        if cpu < 40 and ram < 40:
            # scaling down work when we have more than 1 container
            if len(data['pod']['containers']) > 1:
                # iterate over all container
                for container in data['pod']['containers']:

                    scale_down_container_services_counter = 0
                    if container['id'] == 'c1':
                        scale_down_counter_container = scale_down_counter_container + 1
                        # no need to scale down the first container
                        continue
                    # iterate all the services of a container

                    for service in container['services']:
                        # iterate only once
                        api_path = service["paths"]
                        api_methods = api_path[next(iter(api_path))]

                        for method in api_methods.values():
                            metrics = method["metrics"]["load"]
                            if metrics['load'] < 35:
                                print("cpu => ", cpu, " Ram => ", ram)
                                print("load ", metrics['load'])
                                down_prev_port.append(service['port'])

                                # services that need to be eliminate from the current container
                                scale_down_container_services_counter = scale_down_container_services_counter + 1

                                # overall services need to scale down
                                scale_down_services_counter = scale_down_services_counter + 1
                                # print('need to scaling down, service load is ',metrics['load'])
                            else:
                                down_curr_port.append(service['port'])
                    # eliminate the services from the current container
                    if scale_down_container_services_counter > 0:

                        if len(container['services']) == scale_down_container_services_counter:

                            del template[0]['pod']['containers'][scale_down_counter_container]
                            continue
                        else:
                            print('Services in current container ', down_curr_port)
                            t_new_services = len(container['services']) - scale_down_container_services_counter

                            template[0]['pod']['containers'][scale_down_counter_container][
                                'services'] = get_new_services(t_new_services, down_curr_port)

                    scale_down_counter_container = scale_down_counter_container + 1

                # work when there is 1 or more scaling down services in a container
                if scale_down_services_counter > 0:
                    logger.info('scaling down service to main container')
                    new_services = get_new_services(scale_down_services_counter, down_prev_port)
                    for service in new_services:
                        print(service)
                        template[0]['pod']['containers'][0]['services'].append(service)

                    return template
                else:
                    # this define how many container services need to stay in the current container
                    pass

        # scaling up
        # check if pod's cpu and ram exceeds threshold
        if cpu > 75 and ram > 70:
            # get the list of pod where cpu and ram are greater than 75
            # iterate over all containers of a pod
            for container in data['pod']['containers']:
                container_services_counter = 0
                # if container have one services then move to other container
                if len(container['services']) == 1:
                    counter_container = counter_container + 1
                    continue

                # iterate over to all of the services of a container
                for service in container['services']:
                    # getting the load of services
                    api_path = service["paths"]
                    api_methods = api_path[next(iter(api_path))]

                    for method in api_methods.values():
                        endpoint_load = method["metrics"]["load"]
                        if endpoint_load > 50:
                            new_port.append(service['port'])

                            # to make a filter at container level
                            container_services_counter = container_services_counter + 1
                            # make a filter at pod level.increment service_counter to make a filter so we can add all
                            # the splitting services of one pod into new one container at a time
                            scale_up_services_counter = scale_up_services_counter + 1
                        else:
                            curr_port.append(service['port'])
                # updating the current container services

                if container_services_counter > 0:
                    # true when the splitting services equal to current container actual services
                    if len(container['services']) == container_services_counter:
                        # at least the container must have 1 service remaining in scaling up we are removing the
                        # container in scaling down print(counter_container)
                        template[0]['pod']['containers'][counter_container]['services'] = get_new_services(1, new_port[
                                                                                                              0:1])
                        print('equal scaling up container ', new_port[0:1])
                        new_port = new_port[1:]
                        # minus one service , because we added that one in the parent container
                        scale_up_services_counter = scale_up_services_counter - 1

                    else:
                        services_in_current_container = len(container[
                                                                'services']) - container_services_counter
                        # define the remaining services in the current container
                        # updating the current container services if
                        print('services in remaining ', curr_port)
                        template[0]['pod']['containers'][counter_container]['services'] = get_new_services(
                            services_in_current_container, curr_port)
                counter_container = counter_container + 1

            # creating new containers
            # this works if current container have atleast 1 services remaining

            if scale_up_services_counter > 0:
                print('services in new container', scale_up_services_counter, new_port)
                # create template for new container and its services
                services_in_new_container = get_new_services(scale_up_services_counter, new_port)
                new_container = get_new_container(services_in_new_container)
                template[0]['pod']['containers'].append(new_container)

            # if template changed after monitoring
            if template != copy.deepcopy(config_and_metrics_generator.get_config_file(config_path)):
                return template
            else:
                return False

    if template == copy.deepcopy(config_and_metrics_generator.get_config_file(config_path)):
        # if no changing in the template after monitoring
        return False


def get_new_services(t_services, ports):
    """return json object of new services"""
    verbose_logger.info("getting new services object.")

    print("T-services ", t_services, " Ports ", ports)
    service_template = {'port': '', 'metrics': [{'load': ''}]}
    new_services = []
    for port in ports:
        service_template['port'] = port
        new_services.append(copy.deepcopy(service_template))
    logger.info("getting new services object finished.")

    return new_services


def get_new_container(services):
    """generate a json object of new containers"""

    verbose_logger.info("getting new container object.")
    container_template = {
        'id': 'new Container', 'metrics': {'CPU': '', 'RAM': ''}, 'services': services
    }
    return container_template
