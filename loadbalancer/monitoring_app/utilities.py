import copy

from monitoring_app.models import Method, RefPath, Cluster


def _gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in _gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, (list)):
                for d in v:
                    for result in _gen_dict_extract(key, d):
                        yield result


def _get_schema_only(references):
    saved_schema = 'default'
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            saved_schema = schema[1]
        except IndexError:
            pass

    return saved_schema


def _get_schemas_only(references):
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

            all_references = list(set(_gen_dict_extract('$ref', method)))
            schema_name = _get_schema_only(all_references)

            methods.append(
                Method(path_name, method_name, ref_path, method["x-metrics"]["load"], schema_name, method))
    return clusters, methods


def clean_template(template):
    copied_template = copy.deepcopy(template)
    t_clusters, t_methods = _derive_template_components(copied_template)
    clusters_template = copied_template[RefPath.INFO][RefPath.X_CLUSTERS]

    for cluster in t_clusters:
        for worker_node in cluster.worker_nodes:
            filtered_wn_methods = list(
                filter(lambda method: method.ref_path.worker_node == worker_node.name, t_methods))
            if not filtered_wn_methods:
                print("Deleting worker node:", worker_node.ref_path)
                del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name]
                continue
            for pod in worker_node.pods:
                filtered_pod_methods = list(filter(
                    lambda method: method.ref_path.worker_node == worker_node.name and
                                   method.ref_path.pod_name == pod.name, t_methods))
                if not filtered_pod_methods:
                    print("Deleting pod:", pod.ref_path)
                    del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name][RefPath.PODS][pod.name]
                    continue
                for container in pod.containers:
                    filtered_container_methods = list(filter(
                        lambda method: method.ref_path.worker_node == worker_node.name
                                       and method.ref_path.pod_name == pod.name and
                                       method.ref_path.container_name == container.name, t_methods)
                    )
                    if not filtered_container_methods:
                        print("Deleting container:", container.ref_path)
                        del clusters_template[cluster.name][RefPath.WORKER_NODES][worker_node.name][RefPath.PODS][
                            pod.name][RefPath.CONTAINERS][container.name]
