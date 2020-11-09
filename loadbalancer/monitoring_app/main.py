from .monitoring_service import data_monitor


def monitor_app(docker, kubernetes, service_ports):
    paths = Filepaths()
    paths.default_docker_filepath = docker.defaultDockerFilePath
    paths.docker_deployment_path = docker.deploymentPath
    paths.docker_image = docker.dockerImage
    paths.config_data_path = kubernetes.configDataPath
    paths.yaml_filepath = kubernetes.yamlDeployments
    paths.helm_deployment_path = kubernetes.helmDeployments

    data_monitor(paths, service_ports)
