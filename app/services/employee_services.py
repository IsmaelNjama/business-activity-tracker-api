from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException


from app.models.employee import Employee
from app.schemas.employees import EmployeeUpdate


class EmployeeServices:

    @staticmethod
    def get_all_employees(db: Session) -> List[Employee]:
        return db.query(Employee).all()

    @staticmethod
    def get_employee_by_id(db: Session, id: int) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.id == id).first()

    @staticmethod
    def update_employee(db: Session, id: int, employee_update: EmployeeUpdate) -> Employee:
        employee = EmployeeServices.get_employee_by_id(db, id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee_update_data = employee_update.model_dump(
            exclude_unset=True, by_alias=False)

        if "email" in employee_update_data and employee_update_data["email"] != employee.email:
            existing_employee = db.query(Employee).filter(
                Employee.email == employee_update_data["email"]).first()
            if existing_employee:
                raise HTTPException(
                    status_code=400, detail="Email already registered")

        for field, value in employee_update_data.items():
            setattr(employee, field, value)

        try:
            db.add(employee)
            db.commit()
            db.refresh(employee)
            return employee
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Username or email already exists")

    @staticmethod
    def delete_employee(db: Session, id: int) -> None:
        employee = EmployeeServices.get_employee_by_id(db, id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        try:
            db.delete(employee)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
