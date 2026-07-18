from django.db import models
class Project(models.Model):
    status_choices=[("CP", "Completed"),
                    ("NS","Not Started"),
                    ("IP","In Progress"),
                    ("CA","Cancelled")
                    ]
    name= models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    start_date=models.IntegerField()
    status=models.CharField(max_length=2,choices=status_choices)
   

class Task(models.Model):
    status_choices=[("CP", "Completed"),
                    ("NS","Not Started"),
                    ("IP","In Progress")
                    
                    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    start_date=models.IntegerField()
    status=models.CharField(max_length=2,choices=status_choices)



# Create your models here.
