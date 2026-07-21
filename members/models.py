from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=100)
    company_choices=[("G","Google"),
                     ("M","Microsoft"),
                     ("A","Amazon")]
    company_name=models.CharField(choices=company_choices)
    


    



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
    name=models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    description=models.CharField(max_length=100)
    start_date=models.IntegerField()
    status=models.CharField(max_length=2,choices=status_choices)



    

    
    
# Create your models here.

class User(AbstractUser):
    Role_Choices=[("admin","Admin"),
                  ("employee","Empoyee"),
                  ("manager","Manager")]
    role=models.CharField(max_length=20,choices=Role_Choices)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)