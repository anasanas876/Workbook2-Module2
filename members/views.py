
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project, Task, User, Room, Notes, VersionHistory,Company,WorkSpace,Message
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from .serializer import (
    ProjectSerializer,
    TaskSerializer,
    AuthenticationSerializer,
    UserSerializer,
    RoomSerializer,
    NoteSerializer,
    VersionSerializer,
    CompanySerializer,
    WorkSpaceSerializer,
    MessageSerializer
)
from django.contrib.auth import authenticate

from .Permissions import IsAdmin, IsEmployee, IsManager
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Login Throttle
class LoginThrottle(UserRateThrottle):
    rate = "10/min"



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request):

    filtered_projects = Project.objects.filter(
        company_projects=request.user.company
    )

    serializer = ProjectSerializer(filtered_projects, many=True)

    return Response({
        "Success": True,
        "data": serializer.data
    }, status=200)


# Create Project
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def create_project(request):

    serializer = ProjectSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(company_projects=request.user.company)

        return Response({
            "Success": True,
            "data": serializer.data
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)


# Update Project
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdmin])
def update_project(request, id):

    try:
        project = Project.objects.get(
            id=id,
            company_projects=request.user.company
        )

        serializer = ProjectSerializer(
            project,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                company_projects=request.user.company
            )

            return Response({
                "Success": True,
                "data": serializer.data
            }, status=200)

        return Response({
            "Success": False,
            "data": serializer.errors
        }, status=400)

    except Project.DoesNotExist:
        return Response({
            "Success": False,
            "message": "Project not found."
        }, status=404)


# Delete Project - Soft Delete
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_project(request, id):

    try:
        project = Project.objects.get(
            id=id,
            company_projects=request.user.company
        )

        project.status = "D"
        project.save()

        return Response({
            "Success": True
        }, status=200)

    except Project.DoesNotExist:
        return Response({
            "Success": False,
            "message": "Project does not exist"
        }, status=404)


# Get Tasks
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsManager | IsAdmin])
def get_task(request):

    filtered_tasks = Task.objects.filter(
        company_tasks=request.user.company
    )

    serializer = TaskSerializer(
        filtered_tasks,
        many=True
    )

    return Response({
        "Success": True,
        "data": serializer.data
    }, status=200)


# Create Task
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def create_task(request):

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(
            company_tasks=request.user.company
        )

        return Response({
            "Success": True,
            "data": serializer.data
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)


# Update Task
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdmin | IsManager])
def update_task(request, id):

    try:
        task = Task.objects.get(
            id=id,
            company_tasks=request.user.company
        )

        serializer = TaskSerializer(
            task,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                company_tasks=request.user.company
            )

            return Response({
                "Success": True,
                "data": serializer.data
            }, status=200)

        return Response({
            "Success": False,
            "data": serializer.errors
        }, status=400)

    except Task.DoesNotExist:
        return Response({
            "Success": False,
            "message": "Task not found."
        }, status=404)


# Delete Task - Soft Delete
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdmin | IsManager])
def delete_task(request, id):

    try:
        task = Task.objects.get(
            id=id,
            company_tasks=request.user.company
        )

        task.status = "D"
        task.save()

        return Response({
            "Success": True
        }, status=200)

    except Task.DoesNotExist:
        return Response({
            "Success": False,
            "data": "Task does not exist"
        }, status=404)


# PATCH Task
@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdmin | IsManager])
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
            serializer.save(
                company_tasks=request.user.company
            )

            return Response({
                "Success": True,
                "data": serializer.data
            }, status=200)

        return Response({
            "Success": False,
            "data": serializer.errors
        }, status=400)

    except Task.DoesNotExist:
        return Response({
            "Success": False,
            "message": "Task not found."
        }, status=404)


# Signup
@api_view(["POST"])
def signup(request):

    serializer = AuthenticationSerializer(
        data=request.data
    )

    if serializer.is_valid():

        User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            role=serializer.validated_data["role"],
            company=serializer.validated_data["company"]
        )

        return Response({
            "Success": True,
            "data": serializer.data
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)


# Login
@api_view(["POST"])
         
@permission_classes([AllowAny])      
@throttle_classes([LoginThrottle])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"Success": False, "details": "Username and password are required"},
            status=400,
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"Success": False, "details": "Credentials are invalid"},
            status=401,
        )

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response(
        {
            "Success": True,
            "access": str(access),
            "refresh": str(refresh),
            "company_id": user.company_id,   
            "role": user.role,               
        },
        status=200,
    )


# Employee's Assigned Tasks
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def show_tasks(request, id=None):

    task = Task.objects.filter(
        user_task=request.user,
        company_tasks=request.user.company
    )

    serializer = TaskSerializer(
        task,
        many=True
    )

    return Response({
        "Success": True,
        "data": serializer.data
    }, status=200)


# Only Admins can Create Users
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def create_users(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(
            company=request.user.company
        )

        return Response({
            "Success": True,
            "data": serializer.data
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)


# Only Admins can Delete Users
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_users(request, id):

    try:
        delete_user = User.objects.get(
            id=id,
            company=request.user.company
        )

        delete_user.delete()

        return Response({
            "Success": True,
            "data": "user deleted successfully"
        }, status=200)

    except User.DoesNotExist:
        return Response({
            "Success": False,
            "data": "User does not exist"
        }, status=404)


# Get Rooms
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_rooms(request):

    rooms = Room.objects.filter(workspace_id=request.GET.get("workspace"))

    serializer = RoomSerializer(
        rooms,
        many=True
    )

    return Response({
        "Success": True,
        "data": serializer.data
    }, status=200)


# Create Note
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_note(request):

    serializer = NoteSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            user=request.user
        )

        return Response({
            "Success": True,
            "response": "Note created successfully"
        }, status=201)

    return Response({
        "Success": False,
        "response": serializer.errors
    }, status=400)


# Update Note
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_note(request, id):

    try:
        note = Notes.objects.get(
            id=id,
            user=request.user
        )

        serializer = NoteSerializer(
            note,
            data=request.data
        )
        room_id=f"chat_{note.room.id}"

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            # Get the channel layer
            channel_layer = get_channel_layer()

            # Broadcast the updated note
            async_to_sync(channel_layer.group_send)(
                room_id,
                {
                    "type": "note_update",
                    "text": serializer.data
                }
            )

            return Response({
                "Success": True,
                "data": serializer.data
            }, status=200)

        return Response({
            "Success": False,
            "data": serializer.errors
        }, status=400)

    except Notes.DoesNotExist:
        return Response({
            "Success": False,
            "message": "Note not found."
        }, status=404)



@api_view(["GET"])
def showmessages(request, id):
    room = Room.objects.get(id=id)
    messages = Message.objects.filter(room_id=id).order_by("timestamp")[:20]

    return Response({
        "room": {"id": room.id, "name": room.room_name},
        "messages": list(messages.values("id", "sender", "content", "timestamp"))[::-1],
        "notes": list(Notes.objects.filter(room_id=id)
                  .values("id", "content")),
 }, status=200)
   
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def shownotes(request):

    room_id = request.GET.get("room")

    notes = Notes.objects.filter(room_id=room_id)

    serializer = NoteSerializer(notes, many=True)

    return Response({
        "Success": True,
        "data": serializer.data
    })


    
# Save Version History
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def savehistory(request):

    serializer = VersionSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response({
            "Success": True,
            "data": serializer.data
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)

@api_view(["GET"])
def show_companies(request):

    companies = Company.objects.all()

    serializer = CompanySerializer(companies, many=True)

    return Response({
        "Success": True,
        "data": serializer.data
    }, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_workspace(request):
    serializer=WorkSpaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "Success":True,
            "data":"Workspace Created Successfully"
        },status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_workspaces(request):
    workspace=WorkSpace.objects.all()
    serializer=WorkSpaceSerializer(workspace,many=True)
    return Response(
        {"Success":True,
        "data":serializer.data},status=200
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_room(request):

    serializer = RoomSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            "Success": True,
            "data": "Room created successfully"
        }, status=201)

    return Response({
        "Success": False,
        "data": serializer.errors
    }, status=400)

def accept_files(request):
    return render(request,'index.html')