import logging

VERBOSE_LOGGER = logging.getLogger("mid-verbose")
LOGGER = logging.getLogger("root")


def get_deployment_template(containers_config, wn_name, count):
    VERBOSE_LOGGER.info(f"Started getting deployment for {wn_name}-{str(count)}.")
    tag = containers_config[0]['tag']

    containers = ""
    for container_config in containers_config:
        containers += "\n"
        containers += get_containers(container_config['name'], container_config['image'])

    return f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: config-{tag}-{count}-deployment
  labels: 
    app: config-{tag}-{count}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: config-{tag}-{count}
  template:
    metadata:
      labels:
        app: config-{tag}-{count}
    spec:
      containers:
      {containers}
      nodeSelector: 
        name: {wn_name}
---
apiVersion: v1
kind: Service
metadata:
  name: config-{tag}-{count}-service
spec: 
  selector:
    app: config-{tag}-{count}
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017"""


def get_containers(name, image_name):
    VERBOSE_LOGGER.info(f"Started getting containers config for ${name}.")
    return f"""      - name: {name}
        image: {image_name}"""
