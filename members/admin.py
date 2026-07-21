

from .models import Project, Task,User,Company
from django.contrib import admin


# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Company)
admin.site.register(User)