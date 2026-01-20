
from fastapi import APIRouter, status, Depends, HTTPException, Form
from app.schemas.employees import EmployeeOut, EmployeeCreate
from app.schemas.security import LoginResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.employee import Employee
from typing import Annotated
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from app.utils.security import create_access_token

from app.utils.security import hash_password, verify_password

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/signup", response_model=EmployeeOut)
async def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == employee_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and create employee data
    hashed_password = hash_password(employee_in.password)
    employee_data = employee_in.__dict__.copy()
    employee_data['password'] = hashed_password

    new_employee = Employee(**employee_data)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.post("/login", response_model=LoginResponse)
async def login_employee(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)) -> LoginResponse:
    """Employee login endpoint that returns access token"""
    employee = db.query(Employee).filter(
        Employee.username == username).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not verify_password(password, employee.password):
        raise HTTPException(
            status_code=401, detail="Incorrect password or username")

    access_token_expires = timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES or 30))
    access_token = create_access_token(
        data={"sub": employee.username}, expires_delta=access_token_expires
    )
    return LoginResponse(employee=employee, access_token=access_token, token_type="bearer")
