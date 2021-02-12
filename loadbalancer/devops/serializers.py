import os

from rest_framework import serializers
import json

from devops.models import Project
from monitoring_app.utilities import get_latest_filetag


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    initial_config = serializers.JSONField()
    worker_nodes = serializers.JSONField()


class ProjectModelSerializer(serializers.ModelSerializer):
    config = serializers.SerializerMethodField("_get_configurations")

    def _get_configurations(self, obj):
        config_data_dir = obj.config_data_path
        latest_file_tag = get_latest_filetag(config_data_dir)
        file_name = latest_file_tag + "config.json"
        if latest_file_tag != "00":
            with open(os.path.join(config_data_dir, file_name), "r") as config_file:
                return {"tag": latest_file_tag, "code": json.load(config_file)}

    class Meta:
        model = Project
        fields = ["id", "name", "username", "config"]
