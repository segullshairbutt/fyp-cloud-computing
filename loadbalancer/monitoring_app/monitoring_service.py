import json
import os
import logging

from . import config_and_metrics_generator, monitoring_utility
from .configuration_controller import generate_deployment_files
from .config_and_metrics_generator import get_new_filetag, get_total_files_length, get_latest_filetag
from .deployment_file_templates import generate_configuration_template


VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def generate_related_data(dir_path, config_file, data_file):
    """Get the latest min and max ranges for cpu

    Container and services need this method, because we have to generate new data for the same
    file if monitoring algorithm did not found any exceeding threshold in the specific data.
    Json file new data depend on the previous data last object because in real time there is
    very small variation in resource usage
    """
    VERBOSE_LOGGER.info("getting latest data.")

    with open(os.path.join(dir_path, data_file), 'r') as data:
        content = json.loads(data.read())
    content = content[len(content) - 1]

    first_key = next(iter(content))
    pod = content[first_key]
    pod_cpu = pod['metrics']['CPU']
    pod_ram = pod['metrics']['RAM']

    container = pod['containers']
    container = container[len(container) - 1]
    container_load = container['metrics']['load']

    services = container['services']
    service = services[len(services) - 1]
    # getting the first element of service dict e-g 'paths':{}
    api_path = service["paths"]
    # getting path_name which is first_element e-g 'paths':{'pets':{}}
    api_methods = api_path[next(iter(api_path))]
    # getting first method e-g 'paths':{'pets':{'PUT'{}}}
    method = api_methods[next(iter(api_methods))]
    service_load = method["metrics"]["load"]

    # service_load = api_methods['metrics'][0]['load']
    kwargs = {
        "pod_cpu": pod_cpu,
        "pod_ram": pod_ram,
        "container_load": container_load,
        "service_load": service_load
    }
    config_and_metrics_generator.generate_data(dir_path, config_file, data_file, **kwargs)


def data_monitor(paths, end_points):
    VERBOSE_LOGGER.info("data-monitor started.")

    config_dir_path = paths.config_data_path

    # generating a new file if already doesn't exists
    if get_total_files_length(config_dir_path) == 0:
        initial_template = generate_configuration_template(end_points)
        LOGGER.info("Generating initial files")
        # generate the name for new configuration file
        configfile = str(get_new_filetag(config_dir_path)) + 'config.json'
        # generate the name for new data file
        datafile = str(get_new_filetag(config_dir_path)) + 'data.json'
        # populate new configuration file
        config_and_metrics_generator.write_config_file(initial_template, config_dir_path, configfile)
        # populate new data file
        config_and_metrics_generator.generate_data(config_dir_path, configfile, datafile)

    for run in range(1):
        latest_filetag = str(get_latest_filetag(config_dir_path))
        data_read_file = latest_filetag + 'data.json'
        data_read_path = os.path.join(config_dir_path, data_read_file)
        with open(data_read_path) as f:
            data = f.read()
            dataset = json.loads(data)

        # call monitoring function to check whether data.json file have any object that exceeds
        # threshold, if yes then we need to update the template (config.json file)
        new_template = monitoring_utility.monitor_scaling(dataset, config_dir_path)
        # if false then no change in template occur after monitoring , need to add more objects to the latest
        # data.json file

        if not new_template:
            # no need to update the template just overwrite the new data to latest data.json file
            # add more objects to the latest data.json file
            data_file = str(get_latest_filetag(config_dir_path)) + 'data.json'
            config_file = str(get_latest_filetag(config_dir_path)) + 'config.json'
            generate_related_data(config_dir_path, config_file, data_file)

            LOGGER.info("no changing in template no need to update the config file")
            continue
        else:
            print('--------------------------')
            VERBOSE_LOGGER.info("changes detected, trying to create new configuration")
            # how much containers we need for new template (config.json file)
            LOGGER.info('Total pods: {}'.format(len(new_template[0])))
            for pod in new_template[0].values():
                LOGGER.info('Name: {} Containers: {}'.format(pod["name"], len(pod["containers"])))

            print('--------------------------')
            # generate stuff for new files

            # creating name for new configuration file
            new_config_file = str(get_new_filetag(config_dir_path)) + 'config.json'

            # creating name for new data file
            new_data_file = str(get_new_filetag(config_dir_path)) + 'data.json'

            # creating config.json file with new template
            config_and_metrics_generator.write_config_file(new_template, config_dir_path, new_config_file)

            # creating the data.json file populate data according to new template
            config_and_metrics_generator.generate_data(config_dir_path, new_config_file, new_data_file)

            """create docker files according to how many containers we need in new config
            we are passing prev_files_tags here because at last 2 function that we call above
            already created new files"""

            # generate_deployment_files(config_and_metrics_generator.get_latest_filetag(config_dir_path), paths)
