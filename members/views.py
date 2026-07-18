from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project
from .serializers import ProjectSerializer

# Task 2
@api_view(["GET"])
def project_list(request):
    projects=Project.objects.all()
    
    serializer=ProjectSerializer(projects, many=True)
    return Response(serializer.data)

# Task 3
@api_view(["POST"])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    # Validaates Whether The Recieved data satisfies Model Requirements
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)

# Task 4



@api_view(["PUT"])
def update_project(request, id):
    project = Project.objects.get(id=id)

    serializer = ProjectSerializer(project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
 # Creating End Point For Delete
@api_view(["DELETE"])
def delete_project(request,id):
    project=Project.objects.get(id=id)
    project.delete()

    return Response({"message": "Project deleted successfully"})
# Create your views here.
