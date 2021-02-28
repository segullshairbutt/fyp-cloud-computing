import copy

from constants import CONTAINERS
from monitoring_app.utilities import _derive_template_components


def _get_methods_by_ref_path(methods, ref_path):
    ref_path_methods = {}
    for method in methods:
        if method.ref_path.full_path == ref_path:
            method_path = ref_path_methods.setdefault(method.path_name, {})
            method_path[method.method_name] = method.full_method
    return ref_path_methods


def _get_methods_by_schema(methods, schema):
    schema_methods = {}
    for method in methods:
        if method.schema_name == schema:
            method_path = schema_methods.setdefault(method.path_name, {})
            method_path[method.method_name] = method.full_method
    return schema_methods


def to_template_dto(config, tag):
    copied_template = copy.deepcopy(config)
    clusters, methods = _derive_template_components(copied_template)

    for cluster in clusters:
        for wn in cluster.worker_nodes:
            for pod in wn.pods:
                for container in pod.containers:
                    pod.full_component[CONTAINERS][container.name] = f"{tag}_{cluster.name}_{wn.name}_{pod.name}_{container.name}"
                    # container.full_component['methods'] = _get_methods_by_ref_path(methods, container.ref_path)
    new_template = dict()
    new_template["clusters"] = copied_template["info"]["x-clusters"]
    # for method in methods:
    #     schemas = copied_template.setdefault('schemas', {})
    #     schemas[method.schema_name] = _get_methods_by_schema(methods, method.schema_name)
    return new_template
