import logging

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def get_deployment_template(app_name, containers_config, wn_name, count):
    VERBOSE_LOGGER.info(f"Started getting deployment for {wn_name}-{str(count)}.")
    tag = containers_config[0]['tag']
    app_name = app_name.replace("_", "-")

    app_selector = f"{app_name}-{tag}-{count}"

    containers = ""
    services = ""
    for container_config in containers_config:
        port = container_config["port"]

        name = container_config['name'].replace("_", "-")
        containers += "\n"
        containers += get_containers(name, container_config['image'], port)

        services += "\n"
        services += get_service(name, port, app_selector)

    return f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_selector}-deployment
  labels: 
    app: {app_selector}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {app_selector}
  template:
    metadata:
      labels:
        app: {app_selector}
    spec:
      containers:
      {containers}
      nodeSelector: 
        name: {wn_name}
---
{services}"""


def get_containers(name, image_name, port):
    VERBOSE_LOGGER.info(f"Started getting containers config for {name}.")
    return f"""      - name: {name}
        image: {image_name}
        ports:
        - containerPort: {port}
          name: {name[-2:]}"""


def get_service(name, port, app_selector):
    VERBOSE_LOGGER.info(f"Started getting services for {name}")
    # removing tag from name
    return f"""apiVersion: v1
kind: Service
metadata: 
  name: service-{name}
spec: 
  selector:
    app: {app_selector}
  ports:
  - name: {name[-2:]}
    protocol: TCP
    port: {port}
    targetPort: {port}
    
  type: NodePort
---"""
