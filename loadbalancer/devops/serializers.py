from rest_framework import serializers

from devops.models import Project


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    initial_config = serializers.JSONField()
    worker_nodes = serializers.JSONField()


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "username"]
