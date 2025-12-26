"""Employees auth API endpoints"""
from fastapi import APIRouter
from app.schemas.employees import EmployeeOut, EmployeeCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import HTTPException
from app.models.employee import Employee

from app.utils.security import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=EmployeeOut)
async def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == employee_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Here you would add logic to hash the password and save the employee

    employee_in.password = hash_password(employee_in.password)

    new_employee = Employee(**employee_in.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    print(new_employee)
    return new_employee


@router.post("/login", response_model=EmployeeOut)
async def login_employee(email: str, password: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not verify_password(password, employee.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return employee
