
from rest_framework import serializers
from .models import Project, Task,User





class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
    # Task 5
    def validate_name(self,value):
        if value.strip()=="":
            raise serializers.ValidationError("Project name cannot be empty.")
        return value
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields="__all__"

class AuthenticationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields="__all__"     
                
