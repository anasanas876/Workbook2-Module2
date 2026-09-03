
from rest_framework import serializers
from .models import Project, Task, User, Room, Notes, VersionHistory,Company,WorkSpace


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"

    def validate_name(self, value):
        if value.strip() == "":
            raise serializers.ValidationError(
                "Project name cannot be empty."
            )
        return value


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class AuthenticationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )
    role = serializers.ChoiceField(
        choices=User.Role_Choices
    )
    company = serializers.PrimaryKeyRelatedField(
        queryset=User._meta.get_field("company").remote_field.model.objects.all()
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "role",
            "company"
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False
            }
        }


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }


class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VersionHistory
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields="__all__"

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkSpace
        fields="__all__"