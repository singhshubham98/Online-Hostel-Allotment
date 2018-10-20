from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Diff class for authentication if login user is not hostel admin or Student then
# login page will display error  
class Diff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    is_student = models.BooleanField(default = True)

    def __str__(self):
        return str(self.user)

class Room(models.Model):
    room_no = models.IntegerField(primary_key=True, unique=True)
    block_no = models.CharField(max_length=1, null=True)
    capacity = models.IntegerField(default=3)
    vacancy = models.IntegerField(default=0)

    def __str__(self):
        return str(self.room_no)

class Student(models.Model):
    join_year     = models.IntegerField(default=0)
    room          = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    gender        = models.CharField(max_length = 1)
    age           = models.IntegerField(default=0)
    name          =  models.CharField(max_length = 200, null=True)
    f_name        =  models.CharField(max_length = 200, null=True)
    batch         =  models.IntegerField(default=2016)
    date_of_birth =  models.DateField(null =True, blank = True)
    reg_date      =  models.DateField(null =True)
    fee_receipt   =  models.CharField(max_length = 20, null =True)
    per_address   =  models.TextField(null =True)
    roll_no       = models.CharField(max_length = 10, primary_key =True,unique = True )
    graduate      = models.BooleanField(default = False)

    def __str__(self):
        return str(self.roll_no)

class Change(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason  = models.CharField(max_length = 300)

class Swap(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE)
    student2 = models.CharField(max_length = 100)
    reason   = models.CharField(max_length = 300)
    accept   = models.BooleanField(default = False)
