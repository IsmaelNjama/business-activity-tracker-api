from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.employee_services import EmployeeServices
from app.schemas.employees import EmployeeOut, EmployeeUpdate

router = APIRouter(prefix="/v1/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeOut])
async def get_all_employees(db: Session = Depends(get_db)):
    employees = EmployeeServices.get_all_employees(db)
    return employees


@router.get("/{id}", response_model=EmployeeOut)
async def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    employee = EmployeeServices.get_employee_by_id(db, id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{id}", response_model=EmployeeOut)
async def update_employee(id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = EmployeeServices.update_employee(db, id, employee_update)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id: int, db: Session = Depends(get_db)):
    EmployeeServices.delete_employee(db, id)
    return None
