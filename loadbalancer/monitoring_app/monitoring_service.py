import json
import os
import logging

from . import iterator, data_generator
from .configuration_controller import generate_deployment_files
from .iterator import get_new_filetag1, get_total_files_length, get_prev_filetag1
from .templates import get_initial_configuration_template


verbose_logger = logging.getLogger("mid-verbose")
logger = logging.getLogger("root")


def get_initial_files(dir_path, initial_template):
    verbose_logger.info("getting initial files")
    # generate the name for new configuration file
    configfile = str(get_new_filetag1(dir_path)) + 'config.json'
    # generate the name for new data file
    datafile = str(get_new_filetag1(dir_path)) + 'data.json'
    # populate new configuration file
    iterator.generate_config_file(initial_template, dir_path, configfile)
    # populate new data file
    iterator.generate_data(dir_path, configfile, datafile)


def get_latest_data_object(dir_path, config_file, data_file):
    """Get the latest min and max ranges for cpu

    Container and services need this method, because we have to generate new data for the same
    file if monitoring algorithm did not found any exceeding threshold in the specific data.
    Json file new data depend on the previous data last object because in real time there is
    very small variation in resource usage
    """
    verbose_logger.info("getting latest data object.")

    with open(os.path.join(dir_path, data_file), 'r') as data:
        content = json.loads(data.read())
    content = content[len(content) - 1]
    pod = content['pod']
    pod_cpu = pod['metrics']['CPU']
    pod_ram = pod['metrics']['RAM']

    container = pod['containers']
    container = container[len(container) - 1]
    container_load = container['metrics']['load']

    services = container['services']
    service = services[len(services) - 1]
    service_load = service['metrics'][0]['load']
    iterator.generate_data(dir_path, config_file, data_file, pod_cpu=pod_cpu, pod_ram=pod_ram,
                           container_load=container_load, service_load=service_load)


def data_monitor(paths, service_ports):
    verbose_logger.info("data-monitor started.")

    dir_path = paths.config_data_path

    initial_template = get_initial_configuration_template(service_ports)

    if get_total_files_length(dir_path) == 0:
        get_initial_files(dir_path, initial_template)

    for run in range(50):
        # print('loop',run)
        # pausing loop for 3 seconds
        # get the latest name for data file
        data_read_file = str(get_prev_filetag1(dir_path)) + 'data.json'
        data_read_path = os.path.join(dir_path, data_read_file)
        # print('prev file tag is ',data_read_path)
        # read the latest data.json file
        # read the latest data.json file
        with open(data_read_path) as f:
            data = f.read()
            dataset = json.loads(data)

        # get the latest config file name to monitor
        config_read_file = str(get_prev_filetag1(dir_path)) + 'config.json'

        # creating the path to access the latest config file
        config_read_path = os.path.join(dir_path, config_read_file)

        # call monitoring function to check whether data.json file have any object that exceeds
        # threshold, if yes then we need to update the template (config.json file)
        new_template = data_generator.monitorData(dataset, config_read_path)
        # if false then no change in template occur after monitoring , need to add more objects to the latest
        # data.json file

        if not new_template:
            # no need to update the template just overwrite the new data to latest data.json file
            # add more objects to the latest data.json file
            data_file = str(get_prev_filetag1(dir_path)) + 'data.json'
            config_file = str(get_prev_filetag1(dir_path)) + 'config.json'
            get_latest_data_object(dir_path, config_file, data_file)

            logger.info("no changing in template no need to update the config file")
            continue
        else:
            print('--------------------------')
            verbose_logger.info("changes detected, trying to create new configuration")
            # how much containers we need for new template (config.json file)
            logger.info('total containers {}'.format(len(new_template[0]['pod']['containers'])))
            for container in new_template[0]['pod']['containers']:
                logger.info('Id: {} services: {}'.format(container['id'], len(container['services'])))

            print('--------------------------')
            # generate stuff for new files

            # creating name for new configuration file
            new_config_file = str(get_new_filetag1(dir_path)) + 'config.json'

            # creating name for new data file
            new_data_file = str(get_new_filetag1(dir_path)) + 'data.json'

            # creating config.json file with new template
            iterator.generate_config_file(new_template, dir_path, new_config_file)

            # creating the data.json file populate data according to new template
            iterator.generate_data(dir_path, new_config_file, new_data_file)

            """create docker files according to how many containers we need in new config
            we are passing prev_files_tags here because at last 2 function that we call above
            already created new files"""

            generate_deployment_files(iterator.get_prev_filetag1(dir_path), paths)
