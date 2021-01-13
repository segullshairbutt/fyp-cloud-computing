import copy
import json
import logging
import os

import monitoring_app.data_generator as data_generator
import monitoring_app.templates.config_templates as config_templates
import monitoring_app.utilities as utilities

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

    all_pods = data_file_content["x-pods"]

    first_pod_key = next(iter(all_pods))

    pod = all_pods[first_pod_key]
    pod_cpu = pod['metrics']['CPU']
    pod_ram = pod['metrics']['RAM']

    containers = pod['containers']
    first_container_key = next(iter(containers))
    container = containers[first_container_key]
    container_load = container['metrics']['load']

    first_path_key = next(iter(data_file_content["paths"]))
    first_method_key = next(iter(data_file_content["paths"][first_path_key]))

    method_load = data_file_content["paths"][first_path_key][first_method_key]["x-metrics"]["load"]

    kwargs = {
        "pod_cpu": pod_cpu,
        "pod_ram": pod_ram,
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
        generated_template = config_templates.generate_configuration(project.path_urls.all())
        LOGGER.info("Generating initial files")

        # generate the name for new configuration file
        configfile = str(_get_new_filetag(config_dir_path)) + 'config.json'
        # generate the name for new data file
        datafile = str(_get_new_filetag(config_dir_path)) + 'data.json'
        # populate new configuration file
        _write_config_file(generated_template, config_dir_path, configfile)
        # populate new data file
        # config_and_metrics_generator.generate_data(config_dir_path, configfile, datafile)
        data_generator.generate_data(config_dir_path, configfile, datafile)

        # creating the server side code
        utilities.create_server_stubs(
            os.path.join(project.config_data_path, configfile),
            project.directory,
            helm_chart_path=project.helm_chart_path,
            helm_chart_template_path=project.helm_chart_templates_path,
            helm_deployment_path=project.helm_deployment_path
        )

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
            utilities.create_server_stubs(
                os.path.join(project.config_data_path, new_config_file),
                project.directory,
                helm_chart_path=project.helm_chart_path,
                helm_chart_template_path=project.helm_chart_templates_path,
                helm_deployment_path=project.helm_deployment_path
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
        return "#/info/x-pods/" + self.pod_name + "/containers/" + self.container_name


class Method:
    def __init__(self, path_name, method_name, ref_path, load, full_method):
        self.path_name = path_name
        self.method_name = method_name
        self.ref_path = ref_path
        self.load = load
        self.full_method = full_method

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

    file_name = str(_get_latest_filetag(config_path)) + "config.json"
    template = copy.deepcopy(_get_config_file(os.path.join(config_path, file_name)))
    copied_template = copy.deepcopy(template)

    for single_data_obj in all_data:
        data_paths = single_data_obj["paths"]
        data_pods = single_data_obj["x-pods"]

        number_of_pods = len(data_pods)

        methods = []
        for path_name, path in data_paths.items():
            for method_name, method in path.items():
                ref_path = RefPath(method["x-location"]["$ref"])
                methods.append(Method(path_name, method_name, ref_path, method["x-metrics"]["load"], method))

        for method in methods:
            if MIN_ENDPOINT_LOAD < method.load <= MAX_ENDPOINT_LOAD:
                print("No Need of change {" + method.__str__() + "}")
                continue

            elif method.load > MAX_ENDPOINT_LOAD:
                print("Needed to scale up {" + method.__str__() + "}")

                # checking that the pod have more than one method already deployed.
                number_of_methods_on_pod = _get_number_of_methods_on_path(methods, method.ref_path)
                print("Number of methods on " + method.ref_path.pod_name + ": ", str(number_of_methods_on_pod))

                if number_of_methods_on_pod > 1:
                    new_pod_number = number_of_pods + 1
                    # needed some mechanism to get the port right now i am just adding the pod number to existing port

                    ref_path = method.ref_path
                    # new_port = data_pods[ref_path.pod_name]["containers"][ref_path.container_name][
                    #                "port"] + new_pod_number
                    # print("new port : ", str(new_port))

                    pod_template = _get_pod_template(new_pod_number)

                    pod_name = pod_template["name"]
                    method.ref_path.pod_name = pod_name
                    copied_template["info"]["x-pods"][pod_name] = pod_template
                    # copied_template["paths"][method.path_name][method.method_name]["x-location"][
                    #     "$ref"] = method.ref_path.full_path

                    schema_name = _get_schema_only(list(set(_gen_dict_extract('$ref', method.full_method))))
                    schema_grouped_methods = _get_schema_grouped_methods(methods)

                    # if sum of grouped methods is under threshold methods are grouped together
                    sum_of_schema_group_methods_load = sum(m.load for m in schema_grouped_methods[schema_name])
                    sum_of_schema_group_methods_load += method.load
                    average_of_all_methods = sum_of_schema_group_methods_load / (len(schema_grouped_methods[schema_name]) + 1)

                    LOGGER.info("AVERAGE OF GROUPED METHODS LOAD IS: " + str(average_of_all_methods))
                    if schema_grouped_methods[schema_name] and average_of_all_methods < MAX_ENDPOINT_LOAD:
                        LOGGER.info("methods are grouped in a pod.")
                        generate_template_by_methods(schema_grouped_methods[schema_name], copied_template, pod_name)
                        no_of_methods = len(schema_grouped_methods[schema_name])
                    else:
                        # otherwise a new pod for new method is created..
                        LOGGER.info("creating a new pod for single method.")
                        generate_template_by_methods([method], copied_template, pod_name)
                        no_of_methods = 1

                    # considering the latest number of pods
                    number_of_pods = new_pod_number
                    # decreasing the number of methods on current pod
                    number_of_methods_on_pod -= no_of_methods

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


def generate_template_by_methods(methods, prev_template, pod_name):
    VERBOSE_LOGGER.info("re-writing the config template by using methods..")
    for method in methods:
        method.ref_path.pod_name = pod_name
        prev_template["paths"][method.path_name][method.method_name]["x-location"][
            "$ref"] = method.ref_path.full_path
        LOGGER.info(f"writing {method.path_name}/{method.method_name} on {pod_name}")
    LOGGER.info(f"wrote {str(len(methods))} of method on {pod_name}")


def _gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in _gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in _gen_dict_extract(key, d):
                        yield result


def _get_schema_only(references):
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            return schema[1]
        except IndexError:
            pass
    return 'default'


def _get_schema_grouped_methods(methods):
    schema_methods = {}
    for method in methods:
        all_references = list(set(_gen_dict_extract('$ref', method.full_method)))

        schema_name = _get_schema_only(all_references)

        schema_methods.setdefault(schema_name, [])
        schema_methods[schema_name].append(method)

    return schema_methods


def _get_number_of_methods_on_path(methods, ref_path):
    count = 0
    for method in methods:
        if method.ref_path.full_path == ref_path.full_path:
            count += 1
    return count


def _get_pod_template(number):
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
                }
            }
        }
    }


def _get_path_to_merge(methods, new_load, current_full_ref_path):
    loads = {}
    counters = {}
    for method in methods:
        # adding the load of all methods with same reference path
        load = loads.setdefault(method.ref_path.full_path, new_load)
        load += method.load

        # counting the number of methods on specific reference path
        counter = counters.setdefault(method.ref_path.full_path, 0)
        counter += 1

    for full_ref_path, load in loads.items():
        # we don't want to merge it in current pod.
        if full_ref_path == current_full_ref_path:
            continue

        average = 0

        counter = counters[full_ref_path]
        try:
            average = load / counter
        except ZeroDivisionError:
            print(full_ref_path)
            pass

        # if the loads of any ref_path is less than max endpoint load after addition it will be returned
        if average < MAX_ENDPOINT_LOAD:
            return full_ref_path
    # if no path is capable to take this load None type will be returned
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
