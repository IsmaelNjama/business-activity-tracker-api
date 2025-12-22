"""Employees auth API endpoints"""
from fastapi import APIRouter
from app.schemas.employees import EmployeeOut, EmployeeCreate


router = APIRouter(prefix="/auth", tags=["employees"])


@router.post("/signup", response_model=EmployeeOut)
async def create_employee(employee_in: EmployeeCreate):
    return {"message": "Employee created"}
