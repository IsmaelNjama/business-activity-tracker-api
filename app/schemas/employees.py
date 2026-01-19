from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional


class EmployeeBase(BaseModel):
    """General employee attributes."""
    username: str = Field(..., alias="username")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: EmailStr = Field(..., alias="email")
    phone_number: str = Field(..., alias="phoneNumber")
    gender: str = Field(..., alias="gender")


class EmployeeCreate(EmployeeBase):
    """Employee attributes for registration."""
    model_config = ConfigDict(extra="forbid")
    password: str = Field(..., alias="password")


class EmployeeUpdate(BaseModel):
    """Employee update fields optional"""
    model_config = ConfigDict(extra="forbid")
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")


class EmployeeOut(EmployeeBase):
    """Employee attributes for output."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    role: str
    created_at: datetime


class EmployeeInDB(EmployeeBase):
    id: int
    role: str
    hashed_password: str
