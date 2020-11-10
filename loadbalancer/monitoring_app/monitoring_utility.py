import copy
import logging

from . import metrics_generator

verbose_logger = logging.getLogger("mid-verbose")
logger = logging.getLogger("root")


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


def monitor_data(dataset, config_path):
    """Monitor the metrics of pods , container and services"""
    verbose_logger.info("Monitoring the metrics of pods containers and services.")

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
        template = copy.deepcopy(metrics_generator.get_initial_config(config_path))

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
                        for metrics in service['metrics']:
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
                    for metrics in service['metrics']:
                        if metrics['load'] > 50:
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
            if template != copy.deepcopy(metrics_generator.get_initial_config(config_path)):
                return template
            else:
                return False

    if template == copy.deepcopy(metrics_generator.get_initial_config(config_path)):
        # if no changing in the template after monitoring
        return False
