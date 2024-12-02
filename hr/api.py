from datetime import date
from typing import List
from ninja import NinjaAPI, Router, Schema
from django.shortcuts import get_object_or_404
from .models import Employee, Department


api = NinjaAPI()
router = Router()

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    title: str

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

# Department の作成エンドポイント
@router.post("/departments", response=DepartmentOut)
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return department

# Department の詳細取得エンドポイント
@router.get("/departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department

# 全部門リストの取得エンドポイント
@router.get("/departments", response=List[DepartmentOut])
def list_departments(request):
    qs = Department.objects.all()
    return qs

# 部門の更新エンドポイント
@router.put("/departments/{department_id}", response=DepartmentOut)
def update_department(request, department_id: int, payload: DepartmentIn):
    department = get_object_or_404(Department, id=department_id)
    for attr, value in payload.dict().items():
        setattr(department, attr, value)
    department.save()
    return department

# 部門の削除エンドポイント
@router.delete("/departments/{department_id}", response=dict)
def delete_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return {"success": True}

@router.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@router.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@router.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@router.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@router.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}