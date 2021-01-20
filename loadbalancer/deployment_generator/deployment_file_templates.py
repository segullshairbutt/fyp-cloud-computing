import json


def get_configuration_template():
    return [
        {
            "pod1": {
                "name": "pod1",
                "metrics": {
                    "CPU": "",
                    "RAM": ""
                },
                "containers": [
                    {
                        "id": "c1",
                        "metrics": {
                            "load": "",

                        },
                        "services": []
                    }  # container 1 close
                ]
            }
        }
    ]


def generate_configuration_template(end_points):
    config_object = get_configuration_template()
    services = config_object[0]["pod1"]["containers"][0]["services"]

    for end_point in end_points:
        path = end_point.path
        service_obj = {
            "port": end_point.port,
            "paths": {
                path.name: {}
            }
        }
        for method in path.method_set.all():
            extra_fields = json.loads(method.extra_fields)
            extra_fields["metrics"] = {"load": ""}
            path_name = service_obj["paths"][path.name]
            path_name[method.name] = extra_fields

        services.append(service_obj)
    return config_object


def get_initial_service_content(deployment_name):
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": deployment_name},
        "spec": {
            "selector": {"app": deployment_name},
            "ports": [],
            "type": "LoadBalancer"
        },
    }


def get_initial_deployment_content(deployment_name):
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": deployment_name,
            "labels": {
                "app": deployment_name
            }},
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": deployment_name
                }},
            "template": {
                "metadata":
                    {"labels":
                         {"app": deployment_name}
                     },
                "spec": {
                    "containers": []
                }
            }  # end template
        }  # end selector

    }


def get_container_template():
    return {
        "container": "",
        "image": "",
        "ports": {
            "-containerPort": 3000
        }
    }


def get_docker_image(expose_port):
    return '''FROM node:alpine
WORKDIR /usr/src/app
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE {}
CMD [ "node", "server.js" ]'''.format(expose_port)


def get_service_template():
    return {
        "-protocol": "TCP", "name": "service1", "port": 666, "targetport": 666
    }


def get_values_file_content(docker_image, expose_port, deployment_name):
    return f"""image:
  repository: """ + docker_image + """
  tag: latest
replicaCount: 1
service:
  type: LoadBalancer
  targetPort: """ + str(expose_port) + """
name: """ + deployment_name


def get_chart_file_content(deployment_name):
    return f"""
apiVersion: v2
name: {deployment_name}
type: application
version: 1
"""


def get_deployment_file_content(deployment_name):
    return """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.name }}
  labels:
    app: {{ .Values.name }}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{ .Values.name }}
  template:
    metadata:
      labels:
        app: {{ .Values.name }}
    spec:
      containers:
      - name: container-""" + deployment_name + """
      image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
      ports:
      - containerPort: {{ .Values.service.targetPort }}"""


def get_services_template():
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "{{ .Values.name }}"
        },
        "spec": {
            "selector": {
                "app": "{{ .Values.name }}"
            },
            "ports": [],
            "type": "{{ .Values.service.type }}"

        }
    }
