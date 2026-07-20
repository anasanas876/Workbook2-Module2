from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project
from django.contrib.auth.models import User
from .models import Task
from .serializer import ProjectSerializer, TaskSerializer, AuthenticationSerializer
from django.contrib.auth import authenticate


# Task 2
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):
    projects=Project.objects.all()
    
    serializer=ProjectSerializer(projects, many=True)
    return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )
    


# Task 3
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    # Validaates Whether The Recieved data satisfies Model Requirements
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )
    

    return Response({
        "Success":False,
        "data":serializer.errors
    },
    status=400
    )

# Task 4



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_project(request, id):
    project = Project.objects.get(id=id)

    serializer = ProjectSerializer(project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "Success":True,
            "data":serializer.data
            
        },
        status=200)

    return Response({"Success":False,
                     "data":serializer.errors},
                     status=400)
 # Creating End Point For Delete
@api_view(["DELETE"])
def delete_project(request,id):
    project=Project.objects.get(id=id)
    project.delete()

    return Response({"Success":True},status=200)



# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):
    projects=Task.objects.all()

    serializer=TaskSerializer(projects,many=True)
    return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer=TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":True,
                     "data":serializer.data

    },
    status=201
    )
    return Response ({"Success":False,
                      "data":serializer.errors},
                      status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_project(request,id):
    project=Task.objects.get(id=id)
    serializer=TaskSerializer(project,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )
    return Response({"Success":False,
                     "data":serializer.errors

    },
    status=400
    )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project(request,id):
    project=Task.objects.get(id=id)
    project.delete()
    return Response({"Success":True},status=200)



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_project(request,id):
    task=Task.objects.get(id=id)
    serializer=TaskSerializer(task,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )
    return Response({"Success":False,
                     "data":serializer.errors

    },
    status=400
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signup(request):
    serializer=AuthenticationSerializer(data=request.data)
    if serializer.is_valid():
     
     User.objects.create_user(username=serializer.validated_data["username"],
                              email=serializer.validated_data["email"],
                              password=serializer.validated_data["password"])
     return Response({"Success":True,
                     "data":serializer.data
                     
                     },status=201)
    return Response(
    {
        "Success": False,
        "data": serializer.errors
    },
    status=400
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def login(request):
    serializer=AuthenticationSerializer(data=request.data)
    if serializer.is_valid():
        user=authenticate(
             username=request.data["username"],
             password=request.data["password"]
            
            )
        if user is not None:
            return Response({"Success":True,
                             "Login":"Successful"},
                             status=200)
        else:
            return Response({"Success":False,
                             "Login":"Invalid username or password"},
                             status=401)
        
    return Response(
        serializer.errors,
        status=400
    )


            
        
