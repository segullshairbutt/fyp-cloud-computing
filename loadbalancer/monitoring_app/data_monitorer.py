import copy
import json
import logging
import os

import monitoring_app.data_generator as data_generator
import monitoring_app.templates.config_templates as config_templates
import monitoring_app.utilities as utilities

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
    file_tag = int(dir_size / 2)
    if file_tag < 10:
        file_tag = str("0" + str(file_tag))
    return file_tag


def _generate_related_data(dir_path, config_file, data_file):
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
    # config_and_metrics_generator.generate_data(dir_path, config_file, data_file, **kwargs)
    data_generator.generate_data(dir_path, config_file, data_file, **kwargs)


def data_monitor(project):
    VERBOSE_LOGGER.info("data-monitor started.")

    config_dir_path = project.config_data_path

    # generating a new file if already doesn't exists
    if get_total_files_length(config_dir_path) == 0:
        # generated_template = generate_configuration_template(end_points)
        generated_template = config_templates.generate_configuration(project.path_urls.all())
        LOGGER.info("Generating initial files")

        # generate the name for new configuration file
        configfile = str(get_new_filetag(config_dir_path)) + 'config.json'
        # generate the name for new data file
        datafile = str(get_new_filetag(config_dir_path)) + 'data.json'
        # populate new configuration file
        write_config_file(generated_template, config_dir_path, configfile)
        # populate new data file
        # config_and_metrics_generator.generate_data(config_dir_path, configfile, datafile)
        data_generator.generate_data(config_dir_path, configfile, datafile)

        # creating the server side code
        utilities.create_server_stub(
            os.path.join(project.config_data_path, configfile),
            project.directory,
            helm_chart_path=project.helm_chart_path,
            helm_chart_template_path=project.helm_chart_templates_path)

    for run in range(1):
        latest_filetag = str(get_latest_filetag(config_dir_path))
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
            data_file = str(get_latest_filetag(config_dir_path)) + 'data.json'
            config_file = str(get_latest_filetag(config_dir_path)) + 'config.json'
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
            new_config_file = str(get_new_filetag(config_dir_path)) + 'config.json'

            # creating name for new data file
            new_data_file = str(get_new_filetag(config_dir_path)) + 'data.json'

            # creating config.json file with new template
            write_config_file(new_template, config_dir_path, new_config_file)

            # creating the data.json file populate data according to new template
            data_generator.generate_data(config_dir_path, new_config_file, new_data_file)

            # waiting for 2 seconds so that the file is written succesfully.
            # sleep(2)
            # creating the server side code
            utilities.create_server_stub(
                os.path.join(project.config_data_path, new_config_file),
                project.directory,
                helm_chart_path=project.helm_chart_path,
                helm_chart_template_path=project.helm_chart_templates_path
            )

            """create docker files according to how many containers we need in new config
            we are passing prev_files_tags here because at last 2 function that we call above
            already created new files"""

            # generate_deployment_files(config_and_metrics_generator.get_latest_filetag(config_dir_path), paths)


class RefPath:
    def __init__(self, ref_path):
        paths = ref_path.split("#/info/x-pods/")
        parts = paths[1].split("/")
        self.pod_name = parts[0]
        self.container_name = parts[2]

    @property
    def full_path(self):
        return "#/info/x-pods/" + self.pod_name + "/containers/" + self.container_name + "/port"


class Method:
    def __init__(self, path_name, method_name, ref_path, load):
        self.path_name = path_name
        self.method_name = method_name
        self.ref_path = ref_path
        self.load = load

    def __str__(self):
        return self.path_name + ": " + self.method_name + ", " + str(self.load) + " (" + self.ref_path.full_path + ")"


MAX_ENDPOINT_LOAD = 60
MAX_CPU_USAGE = 75
MAX_RAM_USAGE = 70

MIN_ENDPOINT_LOAD = 25
MIN_CPU_USAGE = 40
MIN_RAM_USAGE = 40


def _monitor_scaling(all_data, config_path):
    VERBOSE_LOGGER.info("Monitor the scaling of pods and containers.")

    file_name = str(get_latest_filetag(config_path)) + "config.json"
    template = copy.deepcopy(get_config_file(os.path.join(config_path, file_name)))
    copied_template = copy.deepcopy(template)

    for single_data_obj in all_data:
        data_paths = single_data_obj["paths"]
        data_pods = single_data_obj["x-pods"]

        number_of_pods = len(data_pods)

        methods = []
        for path_name, path in data_paths.items():
            for method_name, method in path.items():
                ref_path = RefPath(method["x-location"]["$ref"])
                methods.append(Method(path_name, method_name, ref_path, method["x-metrics"]["load"]))

        for method in methods:
            if MIN_ENDPOINT_LOAD < method.load <= MAX_ENDPOINT_LOAD:
                print("No Need of change {" + method.__str__() + "}")
                continue

            elif method.load > MAX_ENDPOINT_LOAD:
                print("Needed to scale up {" + method.__str__() + "}")

                #         checking that the pod have more than one method already deployed.
                number_of_methods_on_pod = _get_number_of_methods_on_path(methods, method.ref_path)
                print("Number of methods on " + method.ref_path.pod_name + ": ", str(number_of_methods_on_pod))

                if number_of_methods_on_pod > 1:
                    new_pod_number = number_of_pods + 1
                    # needed some mechanism to get the port right now i am just adding the pod number to existing port

                    ref_path = method.ref_path
                    new_port = data_pods[ref_path.pod_name]["containers"][ref_path.container_name][
                                   "port"] + new_pod_number
                    print("new port : ", str(new_port))

                    pod_template = _get_pod_template(new_pod_number, new_port)

                    pod_name = pod_template["name"]
                    method.ref_path.pod_name = pod_name
                    copied_template["info"]["x-pods"][pod_name] = pod_template
                    copied_template["paths"][method.path_name][method.method_name]["x-location"][
                        "$ref"] = method.ref_path.full_path

                    #             considering the latest number of pods
                    number_of_pods = new_pod_number
                    #             decreasing the number of methods on current pod
                    number_of_methods_on_pod -= 1

            elif method.load <= MIN_ENDPOINT_LOAD:
                print("Needed to scale down {" + method.__str__() + "}")
                #         here now we will check on which pod we are able to merge this method
                path_to_merge = _get_path_to_merge(methods, method.load, method.ref_path.full_path)
                if not path_to_merge:
                    print("No pod is able to bear the load of this method.")
                else:
                    print("(" + path_to_merge + "): is capable to take the load of {" + method.__str__() + "}")
                    copied_template["paths"][method.path_name][method.method_name]["x-location"]["$ref"] = path_to_merge
                    method.ref_path = RefPath(path_to_merge)

            if copied_template == template:
                print("no changes detected to template.")
                continue
            else:
                print("returning new template")
                _clean_template(methods, copied_template)
                return copied_template

    #     if no new template is made None type is returned back
    return None


def _get_number_of_methods_on_path(methods, ref_path):
    count = 0
    for method in methods:
        if method.ref_path.full_path == ref_path.full_path:
            count += 1
    return count


def _get_pod_template(number, new_port):
    return {
        "name": "pod" + str(number),
        "metrics": {
            "CPU": "",
            "RAM": ""
        },
        "containers": {
            "c1": {
                "id": "c1",
                "metrics": {
                    "load": ""
                },
                "port": new_port
            }
        }
    }


def _get_path_to_merge(methods, new_load, current_full_ref_path):
    loads = {}
    counters = {}
    for method in methods:
        #         adding the load of all methods with same reference path
        load = loads.setdefault(method.ref_path.full_path, new_load)
        load += method.load

        #         counting the number of methods on specific reference path
        counter = counters.setdefault(method.ref_path.full_path, 0)
        counter += 1

    for full_ref_path, load in loads.items():
        #         we don't want to merge it in current pod.
        if full_ref_path == current_full_ref_path:
            continue

        average = 0

        counter = counters[full_ref_path]
        try:
            average = load / counter
        except ZeroDivisionError:
            print(full_ref_path)
            pass

        #         if the loads of any ref_path is less than max endpoint load after addition it will be returned
        if average < MAX_ENDPOINT_LOAD:
            return full_ref_path
    #     if no path is capable to take this load None type will be returned
    return None


def _clean_template(methods, template):
    method_pods = []
    for method in methods:
        method_pods.append(method.ref_path.pod_name)

    method_pods = list(set(method_pods))
    pod_names = list(template["info"]["x-pods"].keys())

    for pod_name in pod_names:
        if pod_name not in method_pods:
            print(pod_name + " don't have any usage, it will be cleaned.")
            del template["info"]["x-pods"][pod_name]
