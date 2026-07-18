
from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
    # Task 5
    def validate_name(self,value):
        if value.strip()=="":
            raise serializers.ValidationError("Project name cannot be empty.")
        return value

