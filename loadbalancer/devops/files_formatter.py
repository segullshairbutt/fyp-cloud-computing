def get_values_file_format(image_name, expose_port, deployment_name):
    return f"""image:
  repository:  {image_name} 
  tag: fyp_kubernetes
replicaCount: 1
service:
  type: LoadBalancer
  targetPort: {expose_port}
name: {deployment_name}
"""


def get_charts_file_format(deployment_name):
    return f"""apiVersion: v2
name: {deployment_name}
type: application
version: 1
"""


def get_deployment_file_format(deployment_name):
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


def get_service_file_format(services_ports):
    return """apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.name }}
spec:
  selector:
    app: {{ .Values.name }}
  ports:
    - protocol: TCP
      name: service1
      port: """ + str(services_ports[0]) + """
      targetPort: {{ .Values.service.targetPort }}
    - protocol: TCP
      name: service2
      port: """ + str(services_ports[1]) + """
      targetPort: {{ .Values.service.targetPort }}
    - protocol: TCP
      name: service3
      port: """ + str(services_ports[2]) + """
      targetPort: {{ .Values.service.targetPort }}
    - protocol: TCP
      name: service4
      port: """ + str(services_ports[3]) + """
      targetPort: {{ .Values.service.targetPort }}
    - protocol: TCP
      name: service5
      port: """ + str(services_ports[4]) + """
      targetPort: {{ .Values.service.targetPort }}
  type: {{ .Values.service.type }}"""