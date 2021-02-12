from rest_framework import views, generics, status
from rest_framework.response import Response

from devops import openapi_service
from devops.models import Project
from devops.serializers import ProjectSerializer, ProjectModelSerializer


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class ProjectDetailView(generics.RetrieveDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    def delete(self, request, *args, **kwargs):
        try:
            openapi_service.delete_project(kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Project with this id not found."})

        return self.destroy(request, *args, **kwargs)


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
            modelSerializer = ProjectModelSerializer(project)
            return Response(status=status.HTTP_201_CREATED, data=modelSerializer.data)


class ProjectMonitoringView(views.APIView):
    def post(self, request, pk):
        try:
            openapi_service.start_monitoring(pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Project with this id not found."})
        return Response(status=status.HTTP_200_OK, data={"info": "Project monitoring started."})