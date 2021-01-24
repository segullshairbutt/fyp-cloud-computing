import operator


class RefPath:
    INITIAL = "#/info/x-clusters/"
    WORKER_NODES = "worker-nodes"
    PODS = "pods"
    CONTAINERS = "containers"
    INFO = "info"
    X_CLUSTERS = "x-clusters"
    X_LOCATION = "x-location"
    REF = "$ref"
    PATHS = "paths"

    def __init__(self, *arg):
        if len(arg) == 1:
            paths = arg[0].split("#/info/x-clusters/")
            parts = paths[1].split("/")
            self.cluster = parts[0]
            self.worker_node = parts[2]
            self.pod_name = parts[4]
            self.container_name = parts[6]
        else:
            self.cluster = arg[0]
            self.worker_node = arg[1]
            self.pod_name = arg[2]
            self.container_name = arg[3]

    @property
    def full_path(self):
        return f"{RefPath.INITIAL}{self.cluster}/{RefPath.WORKER_NODES}/{self.worker_node}/{RefPath.PODS}/" \
               f"{self.pod_name}/{RefPath.CONTAINERS}/{self.container_name}"


class Method:
    def __init__(self, path_name, method_name, ref_path, load, schema_name, full_method):
        self.path_name = path_name
        self.method_name = method_name
        self.ref_path = ref_path
        self.load = load
        self.schema_name = schema_name
        self.full_method = full_method
        self.contribution = 0

    def __str__(self):
        return self.path_name + ": " + self.method_name + " (" + self.ref_path.full_path + ") " + str(
            self.load) + " <-> " + self.schema_name


class Component:
    def __init__(self, name, load, full_component, ref_path=None, is_new=False):
        self.name = name
        self.load = load
        self.full_component = full_component
        self.ref_path = ref_path
        self.is_new = is_new

    def __str__(self):
        return self.name + " ---- " + str(self.load) + " (" + self.ref_path + ") " + "New ? " + str(self.is_new)


class Group:
    def __init__(self, parent_load, sum_of_loads, components):
        self.parent_load = parent_load
        self.sum_of_loads = sum_of_loads
        self.components = components

    def get_contributed_components(self):
        components = []
        for component in self.components:
            component.contribution = (component.load / self.sum_of_loads) * self.parent_load
            components.append(component)
        return sorted(components, key=operator.attrgetter("contribution"))


class Cluster(Component):
    def __init__(self, name, load, full_component, ref_path, is_new=False):
        super().__init__(name, load, full_component, ref_path, is_new)
        self.is_cluster = True

    @property
    def worker_nodes(self):
        worker_nodes = []
        for wn in self.full_component["worker-nodes"].values():
            ref_path = self.ref_path + "/worker-nodes/" + wn["name"]
            worker_nodes.append(WorkerNode(wn["name"], wn["metrics"]["load"], wn, ref_path))
        return worker_nodes


class WorkerNode(Component):
    def __init__(self, name, load, full_component, ref_path, is_new=False):
        super().__init__(name, load, full_component, ref_path, is_new)
        self.is_worker_node = True

    @property
    def pods(self):
        pods = []
        for pod in self.full_component["pods"].values():
            ref_path = self.ref_path + "/pods/" + pod["name"]
            pods.append(Pod(pod["name"], pod["metrics"]["load"], pod, ref_path))
        return pods


class Pod(Component):
    def __init__(self, name, load, full_component, ref_path, is_new=False):
        super().__init__(name, load, full_component, ref_path, is_new)
        self.is_pod = True
        self.contribution = 0

    @property
    def containers(self):
        containers = []
        for container_name, container in self.full_component["containers"].items():
            ref_path = self.ref_path + "/containers/" + container_name
            containers.append(Container(container_name, container["metrics"]["load"], container, ref_path))
        return containers


class Container(Component):
    def __init__(self, name, load, full_component, ref_path, is_new=False):
        super().__init__(name, load, full_component, ref_path, is_new)
        self.is_container = True


class PodGroup(Group):
    def __init__(self, parent_load, sum_of_loads, components):
        super().__init__(parent_load, sum_of_loads, components)
        self.is_pod_group = True

    def __str__(self):
        return "PodGroup sum_of_loads: " + str(self.sum_of_loads)


class ContainerGroup(Group):
    def __init__(self, parent_load, sum_of_loads, components):
        super().__init__(parent_load, sum_of_loads, components)
        self.is_container_group = True

    def __str__(self):
        return "ContainerGroup sum_of_loads: " + str(self.sum_of_loads)


class MethodGroup(Group):
    def __init__(self, parent_load, sum_of_loads, components):
        super().__init__(parent_load, sum_of_loads, components)
        self.is_method_group = True

    def __str__(self):
        return "ContainerGroup sum_of_loads: " + str(self.sum_of_loads)
