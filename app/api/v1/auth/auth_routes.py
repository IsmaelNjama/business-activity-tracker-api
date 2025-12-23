"""Employees auth API endpoints"""
from fastapi import APIRouter
from app.schemas.employees import EmployeeOut, EmployeeCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import HTTPException
from app.models.employee import Employee


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=EmployeeOut)
async def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == employee_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Here you would add logic to hash the password and save the employee
    new_employee = Employee(**employee_in.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
