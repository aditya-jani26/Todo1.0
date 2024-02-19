from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=500, unique=True)
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.name
# =================================================================   
class Todo(models.Model):
    user_id= models.ForeignKey(Person,on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    completed = models.BooleanField(default=0)
    # status = models.CharField(max_length=10, null=True, blank=True,default='In progress')
    

    def __str__(self):
        return str(self.title)
