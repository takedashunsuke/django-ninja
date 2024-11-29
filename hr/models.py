from django.db import models

from accounts.models import UserAccount

# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    # user = models.OneToOneField(
    #     UserAccount, 
    #     on_delete=models.CASCADE, 
    #     related_name='employee'
    # )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cv = models.FileField(null=True, blank=True)
