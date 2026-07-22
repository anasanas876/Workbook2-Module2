from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project,Task,User


from .serializer import ProjectSerializer, TaskSerializer, AuthenticationSerializer,UserSerializer
from django.contrib.auth import authenticate

from .Permissions import IsAdmin,IsEmployee




# Task 2 Module 5
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):
    filtered_projects=Project.objects.filter(company_projects=request.user.company)
    
    
    serializer=ProjectSerializer(filtered_projects, many=True)
    return Response({"Success":True,
                     "data":serializer.data

    },
    status=200
    )
    


# Task 3,4,5 (Status Codes, Response Format) Module 5
@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdmin])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(company_projects=request.user.company)
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

# Task 4 & 5 Module 5 (Updating Resource & Response Format Consitency)


# Task 3 Module 5
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdmin])
def update_project(request, id):
    try:
        project = Project.objects.get(
            id=id,
            company_projects=request.user.company
        )

        serializer = ProjectSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save(company_projects=request.user.company)

            return Response(
                {
                    "Success": True,
                    "data": serializer.data
                },
                status=200
            )
        return Response({"Success":False,
                         "data":serializer.errors},status=400)

        
    except Project .DoesNotExist:
        return Response(
            {
                "Success": False,
                "message": "Project not found."
            },
            status=404
        )

 # Creating End Point For Delete
@api_view(["DELETE"])
@permission_classes([IsAdmin,IsAuthenticated])
def delete_project(request,id):
    try:
     project=Project.objects.get(id=id,company_projects=request.user.company)
     project.delete()

     return Response({"Success":True},status=200)
    except Project .DoesNotExist:
     return Response({"Succuess":False},
                     status=403)






# Get Endpoint for Tasks Task 1 Module 5
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request):
    
    filtered_tasks = Task.objects.filter(company_tasks=request.user.company)

    serializer = TaskSerializer(filtered_tasks, many=True)

    return Response(
        {
            "Success": True,
            "data": serializer.data
        },
        status=200
    )
# Task 2 ,4&5  Module 5 (Response Formats and status code)
# POST Endpoints for Tasks
@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdmin])
def create_task(request):
    serializer=TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(company_tasks=request.user.company)
        return Response({"Success":True,
                     "data":serializer.data

    },
    status=201
    )
    return Response ({"Success":False,
                      "data":serializer.errors},
                      status=400)

# PUt Endpoint for Tasks
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdmin])
def update_task(request, id):
    try:
        project = Task.objects.get(
            id=id,
            company_tasks=request.user.company
        )

        serializer = TaskSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save(company_tasks=request.user.company)

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

    except Task.DoesNotExist:
        return Response(
            {
                "Success": False,
                "message": "Task not found."
            },
            status=404
        )

# Delete endpoint for Tasks
@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdmin])
def delete_task(request,id):
    try:
    
     project=Task.objects.get(id=id,company_tasks=request.user.company)
     project.delete()
     return Response({"Success":True},status=200)
    except Task.DoesNotExist:
        return Response({"Success":False,
                         "data":"Task does not exist"},status=404)
    
    


# PATCH Endpoint for Tasks
@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdmin])
def partially_update_task(request, id):
    try:
        task = Task.objects.get(
            id=id,
            company_tasks=request.user.company
        )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save(company_tasks=request.user.company)

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

    except Task.DoesNotExist:
        return Response(
            {
                "Success": False,
                "message": "Task not found."
            },
            status=404
        )

# Signup Endpoint Module 6
@api_view(["POST"])

def signup(request):
    serializer=AuthenticationSerializer(data=request.data)
    if serializer.is_valid():
     
     User.objects.create_user(username=serializer.validated_data["username"],
                              email=serializer.validated_data["email"],
                              password=serializer.validated_data["password"],
                              role=serializer.validated_data["role"])
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






    



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_tasks(request,id):
    if request.user.role=="employee": 
     
      task=Task.objects.filter(user_task=request.user)
      serializer=TaskSerializer(task,many=True)

      return Response({"Succuess":True,
                     "data":serializer.data},
                     status=200)
    else:
        return Response("This Section Belongs to employee only.")
      

 # Allow only Admins to Create Users(Task 2)
@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdmin])
def create_users(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success":True,
                        "data":serializer.data},status=201)
    return Response({"Success":False,
                     "data":serializer.errors},status=400)
# allow Admins only to Delete Users(Task 2)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdmin])
def delete_users(request,id):
      try:
     
        delete_user=User.objects.get(id=id)
        delete_user.delete()
        return Response({"Success":True,
                       "data":"user deleted successfully"},status=200)
      except User.DoesNotExist:
          return Response({"Success":False,
                           "data":"User does not exist"},status=404

                           )


# Task 2 & 4 Module 7 Get Endpoint for Company Specific Projects:

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_company_specific_projects(request):
    
        projects=Project.objects.filter(company_projects=request.user.company)
        serializer=ProjectSerializer(projects,many=True)
        return Response({"Success":True,
                        "data":serializer.data},
                        status=200)

# task 2 & 4 Module 7
# Get Endpoint for Company Specific Task:
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_company_specific_tasks(request):
    
        tasks=Task.objects.filter(company_tasks=request.user.company)
        serializer=TaskSerializer(tasks,many=True)
        return Response({"Success":True,
                        "data":serializer.data},
                        status=200)
    




            
        
