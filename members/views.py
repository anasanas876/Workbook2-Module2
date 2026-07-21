from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project

from .models import Task,User
from .serializer import ProjectSerializer, TaskSerializer, AuthenticationSerializer,UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .Permissions import IsAdmin,IsEmployee

User = get_user_model()


# Task 2
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):
    filtered_projects=Project.objects.filter(company=request.user.company)
    
    
    serializer=ProjectSerializer(filtered_projects, many=True)
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





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request):
    filtered_tasks = Task.objects.filter(company=request.user.company)

    serializer = TaskSerializer(filtered_tasks, many=True)

    return Response(
        {
            "Success": True,
            "data": serializer.data
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

@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdmin])
def create_task(request):
    serialization=TaskSerializer(data=request.data)
    if serialization.is_valid():
        serialization.save()
        return Response({"Succuess":True,
                         "data":serialization.data},
                         status=201)
    return Response({"Succuess":False,
                     "data":serialization.errors},status=400)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdmin])
def update_task(request, id):
    task = Task.objects.get(id=id)

    serializer = TaskSerializer(
        task,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "Success": True,
                "data": serializer.data
            },
            status=200
        )

    return Response(
        {
            "Success": False,
            "data": serializer.errors
        },
        status=400
    )
@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdmin])
def delete_task(request,id):
    task=Task.objects.get(id=id)
    task.delete()


@api_view(["GET"])
@permission_classes([IsAuthenticated,IsEmployee])
def show_tasks(request,id):
    task=Task.objects.get(id=id)
    serializer=TaskSerializer(task)
    return Response({"Succuess":True,
                     "data":serializer.data},
                     status=200)
 

            
        
