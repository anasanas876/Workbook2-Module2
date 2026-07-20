

from .models import Project, Task
from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
