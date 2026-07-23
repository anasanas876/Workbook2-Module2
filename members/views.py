from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project,Task,User,AuditLog
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes

# Ineriting LoginThrottle from UserRateThrottle
class LoginThrottle(UserRateThrottle):
    rate="10/min"
    




from .serializer import ProjectSerializer, TaskSerializer, AuthenticationSerializer,UserSerializer
from django.contrib.auth import authenticate

from .Permissions import IsAdmin,IsEmployee




# Task 2 Module 5
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):
    filtered_projects=Project.objects.filter(company_projects=request.user.company)
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Requested to give all projects")
    audit.save()
    audit.related_object("projects")
    audit.save()
    

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
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Requested to Create projects")
    audit.save()
    audit.related_object("Create Projects")
    audit.save()
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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("User Requested to Update Projects")
        audit.save()
        audit.related_object("Update Projects")
        audit.save()


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
     project.status("NS")
     audit=AuditLog()
     audit.user(f"User{request.user}")
     audit.save()
     audit.action("User Requested to delete Project")
     audit.save()
     audit.related_object("Delete Projects")
     audit.save()

     return Response({"Success":True},status=200)
    except Project .DoesNotExist:
     return Response({"Succuess":False},
                     status=403)






# Get Endpoint for Tasks Task 1 Module 5
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request):
    
    filtered_tasks = Task.objects.filter(company_tasks=request.user.company)
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Requested to Give all Authorized Tasks")
    audit.save()
    audit.related_object("Give Tasks")
    audit.save()

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
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Requested to create new Task")
    audit.save()
    audit.related_object("Create New Task")
    audit.save()
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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("User Requested to update task")
        audit.save()
        audit.related_object("Update Task")
        audit.save()

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

# Delete endpoint for Tasks(Modified it by implementing Soft Delete)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdmin])
def delete_task(request,id):
    try:
    
     task=Task.objects.get(id=id,company_tasks=request.user.company)
     task.status("NS")
     task.save()
     audit=AuditLog()
     audit.user(f"User{request.user}")
     audit.save()
     audit.action("User Requested to delete a task")
     audit.save()
     audit.related_object("Delete Task")
     audit.save()
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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("User Requested to partially update a task")
        audit.save()
        audit.related_object("Partially Update Tasks")
        audit.save()

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
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Signed Up")
    audit.save()
    audit.related_object("Signup")
    audit.save()
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

@api_view(["POST"])
@throttle_classes([LoginThrottle])
def login(request):
    username,password=request.data["username"],request.data["password"]
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("User Requested for Log In.")
    audit.save()
    audit.related_object("projects")
    audit.save()
   
    user=authenticate(username=username,password=password)
        # As it returns None if credentials are invalid
    if user is None:
            return Response({"Success":False,
                            "details":"Credentials are invalid"},status=401)
    else:
            refresh=RefreshToken.for_user(user)
            access=refresh.access_token
            return Response({"Success":True,
                             "access":access,
                             "refresh":refresh},status=200)
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_tasks(request,id):
    audit=AuditLog()
    audit.user(f"User{request.user}")
    audit.save()
    audit.action("Employee requested to show their assigned tasks")
    audit.save()
    audit.related_object("Show Assigned Tasks")
    audit.save()
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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("Admin Created User")
        audit.save()
        audit.related_object("Create User")
        audit.save()
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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("Admin requested for Company Specific Projects")
        audit.save()
        audit.related_object("Get Specific Projects")
        audit.save()

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
        audit=AuditLog()
        audit.user(f"User{request.user}")
        audit.save()
        audit.action("Admin Requested to get Specific Tasks")
        audit.save()
        audit.related_object("Get Specific Tasks")
        audit.save()
    




            
        
