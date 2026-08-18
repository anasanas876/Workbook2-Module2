from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),

    # Projects
    path("projects/", views.project_list, name="project_list"),
    path("projects/create/", views.create_project, name="create_project"),
    path("projects/update/<int:id>/", views.update_project, name="update_project"),
    path("projects/delete/<int:id>/", views.delete_project, name="delete_project"),

    # Tasks
    path("tasks/", views.get_task, name="get_task"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/update/<int:id>/", views.update_task, name="update_task"),
    path("tasks/delete/<int:id>/", views.delete_task, name="delete_task"),
    path("tasks/patch/<int:id>/", views.partially_update_task, name="partially_update_task"),

    # Employee Tasks
    path("tasks/assigned/<int:id>/", views.show_tasks, name="show_tasks"),

    # Users
    path("users/create/", views.create_users, name="create_users"),
    path("users/delete/<int:id>/", views.delete_users, name="delete_users"),
    path("users/getrooms/",views.get_rooms,name="get_rooms")
]