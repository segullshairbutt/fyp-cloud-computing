from rest_framework import views, generics, status
from rest_framework.response import Response

from devops import openapi_service
from devops.serializers import ProjectSerializer, ProjectModelSerializer


class ProjectCreateView(views.APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        else:
            data = serializer.data
            try:
                project = openapi_service.create_project(
                    data["name"], data["initial_config"], data["worker_nodes"])
            except IsADirectoryError:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error": "A project with this name already exists."})
            modelSerializer = ProjectModelSerializer(data=project)
            return Response(status=status.HTTP_201_CREATED, data=modelSerializer.initial_data)