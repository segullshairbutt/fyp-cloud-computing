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
    ingress_rules = ""
    istio_matches = ""
    for container_config in containers_config:
        port = container_config["port"]

        name = container_config['name'].replace("_", "-")
        containers += "\n"
        containers += get_containers(name, container_config['image'], port)

        services += "\n"
        services += get_service(name, port, app_selector)

        context_path = container_config["context_path"]

        ingress_rules += get_ingress_rule(context_path, name, port)

        istio_matches += get_istio_match(context_path, name, port)

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
{services}
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress2
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  {ingress_rules}
---

apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: istio-project-gateway
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
---

apiVersion: networking.istio.io/v1alpha3

kind: VirtualService

metadata:
  name: {app_selector}
spec:
  hosts:
  - "*"
  gateways:
  - istio-project-gateway
  http:
  {istio_matches}
"""


def get_containers(name, image_name, port):
    VERBOSE_LOGGER.info(f"Started getting containers config for {name}.")
    return f"""      - name: {name}
        image: {image_name}
        imagePullPolicy: Always
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
  labels: 
    app: {app_selector}
spec: 
  selector:
    app: {app_selector}
  ports:
  - name: {name[-2:]}
    protocol: TCP
    port: {port}
    targetPort: {port}
---"""


def get_ingress_rule(path, service_name, port):
    return f"""
  - http:
      paths:
      - path: /{path}
        backend:
          serviceName: service-{service_name}
          servicePort: {port}"""


def get_istio_match(path, service_name, port):
    return f"""
  - match:
    - uri:
        prefix: /{path}
    route:
    - destination:
        host: service-{service_name}
        port:
          number: {port}"""
