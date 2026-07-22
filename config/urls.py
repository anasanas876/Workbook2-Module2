"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from members import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path("projects/", views.project_list, name="project_list"),
    path("createprojects/", views.create_project, name="create_project"),
    path("updateprojects/<int:id>/", views.update_project, name="update_project"),
    path("deleteproject/<int:id>/", views.delete_project, name="delete_project"),
    path("tasks/", views.get_task, name="get_task"),
    path("createtasks/", views.create_task, name="create_task"),
    path("updatetasks/<int:id>/", views.update_task, name="update_task"),
    path("patchtasks/<int:id>/", views.partially_update_task, name="partially_update_task"),
    path("deletetasks/<int:id>/", views.delete_task, name="delete_task"),
    path("showtasks/<int:id>/", views.show_tasks, name="show_tasks"),
    path("createusers/", views.create_users, name="create_users"),
    path("deleteusers/<int:id>/", views.delete_users, name="delete_users"),
    path("specificprojects/",views.get_company_specific_projects, name="company_projects"),
    path("specifictasks/",views.get_company_specific_tasks,name="company_tasks"),
            
    ]