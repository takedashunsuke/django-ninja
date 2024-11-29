from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Department, Employee

# Register your models here.
admin.site.register(Department)
admin.site.register(Employee)