from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_empolyee = models.BooleanField(default=False)


class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username



class EmployeeStatus(models.Model):
    type_tuple = (
        (1, 'M'),
        (2, 'A'),
        (3, 'N'),
        (4, 'On Call'),
        (5, 'Sleap'),
        (6, 'OFF Day'),
    )
    day=models.DateField()
    type=models.IntegerField(
        choices=type_tuple,
        default=6
    )
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='cases')


class workHours(models.Model):
    status=models.OneToOneField(EmployeeStatus,on_delete=models.CASCADE , related_name='workhours')
    breakNum=models.IntegerField(default=0)
    one=models.BooleanField(default=True)
    two=models.BooleanField(default=True)
    three=models.BooleanField(default=True)
    four=models.BooleanField(default=True)
    five=models.BooleanField(default=True)
    six=models.BooleanField(default=True)
    seven=models.BooleanField(default=True)
    eight=models.BooleanField(default=True)


class SwapRequest(models.Model):
    owner=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='SwapRequestOwners')
    shift=models.OneToOneField(EmployeeStatus,on_delete=models.CASCADE)
    answer=models.BooleanField(default=False)
    users=models.ManyToManyField(Employee,related_name='SwapRequests')
