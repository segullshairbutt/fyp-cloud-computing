import copy
import os

from monitoring_app.models import Method, RefPath, Cluster


def gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, (list)):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result


def get_schema_only(references):
    saved_schema = 'default'
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            saved_schema = schema[1]
        except IndexError:
            pass

    return saved_schema


def get_schemas_only(references):
    saved_schemas = []
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            saved_schemas.append(schema[1])
        except IndexError:
            pass

    return saved_schemas


def _join_components(threshold, components):
    joined_components = []
    remaining_components = []
    collective_contribution = 0
    for i in range(len(components)):
        component = components[i]
        collective_contribution += component.contribution

        if collective_contribution < threshold:
            joined_components.append(component)
        else:
            remaining_components.append(component)

    return joined_components, remaining_components


def _derive_template_components(template):
    clusters = []
    cls = template[RefPath.INFO][RefPath.X_CLUSTERS]

    for cl in cls.values():
        ref_path = RefPath.INITIAL + cl["name"]
        clusters.append(Cluster(cl["name"], cl["metrics"]["load"], cl, ref_path))

    methods = []
    data_paths = template[RefPath.PATHS]
    for path_name, path in data_paths.items():
        for method_name, method in path.items():
            ref_path = RefPath(method[RefPath.X_LOCATION][RefPath.REF])

            all_references = list(set(gen_dict_extract('$ref', method)))
            schema_name = get_schema_only(all_references)

            methods.append(
                Method(path_name, method_name, ref_path, method["x-metrics"]["load"], schema_name, method))
    return clusters, methods


def clean_template(template):
    t_clusters, t_methods = _derive_template_components(template)
    clusters_template = template[RefPath.INFO][RefPath.X_CLUSTERS]

    for cluster in t_clusters:
        for worker_node in cluster.worker_nodes:
            filtered_wn_methods = list(
                filter(lambda method: method.ref_path.worker_node == worker_node.name, t_methods))
            if not filtered_wn_methods:
                print("Deleting worker node:", worker_node.ref_path)
                del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name]
                # continue
            for pod in worker_node.pods:
                filtered_pod_methods = list(filter(
                    lambda method: method.ref_path.worker_node == worker_node.name and
                                   method.ref_path.pod_name == pod.name, t_methods))
                if not filtered_pod_methods:
                    print("Deleting pod:", pod.ref_path)
                    del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name][RefPath.PODS][pod.name]
                    # continue
                for container in pod.containers:
                    filtered_container_methods = list(filter(
                        lambda method: method.ref_path.worker_node == worker_node.name and method.ref_path.pod_name == pod.name and method.ref_path.container_name == container.name,
                                                             t_methods))
                    if not filtered_container_methods:
                        print("Deleting container:", container.ref_path)
                        del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name][RefPath.PODS][
                            pod.name][RefPath.CONTAINERS][container.name]


def reorder_template(template):
    c_template = copy.deepcopy(template)
    # cc_template = copy.deepcopy(template)

    c_clusters_template = c_template[RefPath.INFO][RefPath.X_CLUSTERS]
    cc_clusters_template = template[RefPath.INFO][RefPath.X_CLUSTERS]

    c_clusters, c_methods = _derive_template_components(c_template)

    for r_cl in range(len(c_clusters)):
        cl = c_clusters[r_cl]
        cl_name = "cl" + str(r_cl + 1)
        if cl.name == cl_name:
            pass
        else:
            cl_value = c_clusters_template[cl.name]
            cl_value['name'] = cl_name
            cc_clusters_template[cl_name] = cl_value

            cl_methods = filter(lambda m: m.ref_path.cluster == cl.name, c_methods)
            for method in cl_methods:
                print("Changed from:", method.ref_path.full_path)
                method.ref_path.cluster = cl_name
                method.full_method['x-location'][RefPath.REF] = method.ref_path.full_path
                print("To:", method.ref_path.full_path)

                template[RefPath.PATHS][method.path_name][method.method_name] = method.full_method

            del c_clusters_template[cl.name]
            cl.name = cl_name

        for r_wn in range(len(cl.worker_nodes)):
            wn = cl.worker_nodes[r_wn]
            wn_name = "wn" + str(r_wn + 1)
            if wn.name == wn_name:
                pass
            else:
                wn_value = c_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name]
                wn_value['name'] = wn_name

                cc_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name] = wn.full_component

                wn_methods = filter(
                    lambda m: m.ref_path.cluster == cl.name and m.ref_path.worker_node == wn.name,
                    c_methods)
                for method in wn_methods:
                    print("Changed from:", method.ref_path.full_path)
                    method.ref_path.worker_node = wn_name
                    method.full_method['x-location'][RefPath.REF] = method.ref_path.full_path
                    print("To:", method.ref_path.full_path)

                    template[RefPath.PATHS][method.path_name][method.method_name] = method.full_method

                del c_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name]
                wn.name = wn_name

            for r_pod in range(len(wn.pods)):
                pod = wn.pods[r_pod]
                pod_name = "pod" + str(r_pod + 1)

                if pod.name == pod_name:
                    pass
                else:
                    pod_value = c_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][RefPath.PODS][pod.name]
                    pod_value['name'] = pod_name

                    cc_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][RefPath.PODS][pod_name] = pod_value

                    pod_methods = filter(lambda
                                             m: m.ref_path.cluster == cl.name and m.ref_path.worker_node == wn.name and m.ref_path.pod_name == pod.name,
                                         c_methods)
                    for method in pod_methods:
                        print("Changed from:", method.ref_path.full_path)
                        method.ref_path.pod_name = pod_name
                        method.full_method['x-location'][RefPath.REF] = method.ref_path.full_path
                        print("To:", method.ref_path.full_path)

                        template[RefPath.PATHS][method.path_name][method.method_name] = method.full_method

                    del cc_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][RefPath.PODS][pod.name]
                    pod.name = pod_name
                for r_container in range(len(pod.containers)):
                    container = pod.containers[r_container]
                    container_name = "c" + str(r_container + 1)
                    if container.name == container_name:
                        pass
                    else:
                        container_value = c_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][
                            RefPath.PODS][pod.name][RefPath.CONTAINERS][container.name]
                        container_value['id'] = container_name

                        cc_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][RefPath.PODS][pod.name][
                            RefPath.CONTAINERS][container_name] = container_value

                        containers_methods = filter(lambda m: m.ref_path.cluster == cl.name
                                                              and m.ref_path.worker_node == wn.name
                                                              and m.ref_path.pod_name == pod.name
                                                              and m.ref_path.container_name == container.name,
                                                    c_methods)
                        for method in containers_methods:
                            print("Changed from:", method.ref_path.full_path)
                            method.ref_path.container_name = container_name
                            method.full_method['x-location'][RefPath.REF] = method.ref_path.full_path
                            print("To:", method.ref_path.full_path)

                            template[RefPath.PATHS][method.path_name][method.method_name] = method.full_method

                        del cc_clusters_template[cl.name][RefPath.WORKER_NODES][wn.name][RefPath.PODS][pod.name][
                            RefPath.CONTAINERS][container.name]
                        container.name = container_name


def get_latest_filetag(dir_path):
    """get the number of latest configuration file"""

    dir_size = (len(os.listdir(dir_path)))
    file_tag = int(dir_size / 2)
    if file_tag < 10:
        file_tag = str("0" + str(file_tag))
    return file_tag
