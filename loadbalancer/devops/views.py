import os

from django.http import HttpResponse
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from devops import openapi_service
from devops.models import Project
from devops.serializers import ProjectSerializer, ProjectModelSerializer
from devops.resources_service import get_latest_filetag


class ProjectListView(generics.ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ProjectModelSerializer

    def get_queryset(self):
        return Project.objects.filter(username=self.request.user.username)


class ProjectDetailView(generics.RetrieveDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    def delete(self, request, *args, **kwargs):
        try:
            openapi_service.delete_project(kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Project with this id not found."})

        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
def get_deployments_download_link(request, project_id):
    project = Project.objects.get(id=project_id)
    file_tag = get_latest_filetag(project.helm_deployment_path)
    if file_tag == "00":
        response = Response({"error": "No configuration exists yet."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        file_path = os.path.join(project.helm_deployment_path, file_tag + "config")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        else:
            response = Response({"error": "No configuration exists yet."}, status=status.HTTP_400_BAD_REQUEST)
    return response


class ProjectCreateView(views.APIView):
    permission_classes = IsAuthenticated,

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        else:
            data = serializer.data
            try:
                project = openapi_service.create_project(
                    request.user.username, data["name"], data["initial_config"])
            except IsADirectoryError:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error": "A project with this name already exists."})
            modelSerializer = ProjectModelSerializer(project)
            return Response(status=status.HTTP_201_CREATED, data=modelSerializer.data)


class ProjectMonitoringView(views.APIView):
    def post(self, request, pk):
        try:
            openapi_service.start_monitoring(pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Project with this id not found."})
        return Response(status=status.HTTP_200_OK, data={"info": "Project monitoring started."})


class ProjectConfigView(views.APIView):
    def get(self, request, pk, config_key):
        return Response(openapi_service.get_config_file(pk, config_key))
