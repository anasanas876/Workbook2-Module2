from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    
    company_choices=[("G","Google"),
                     ("M","Microsoft"),
                     ("A","Amazon")]
    company_name=models.CharField(max_length=25,choices=company_choices)

    def __str__(self):
        return self.company_name
    


    



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
    company_projects=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
   

class Task(models.Model):
    status_choices=[("CP", "Completed"),
                    ("NS","Not Started"),
                    ("IP","In Progress")
                    
                    ]
    name=models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company_tasks=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    user_task=models.ForeignKey("User",on_delete=models.CASCADE,null=True)
    description=models.CharField(max_length=100)
    start_date=models.IntegerField()
    status=models.CharField(max_length=2,choices=status_choices)

    def __str__(self):
        return self.name
    



    
class User(AbstractUser):
    Role_Choices=[("admin","Admin"),
                  ("employee","Empoyee"),
                  ("manager","Manager")]
    role=models.CharField(max_length=20,choices=Role_Choices)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    
    
    
