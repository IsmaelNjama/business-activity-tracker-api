from pydantic import BaseModel, EmailStr, ConfigDict


class EmployeeBase(BaseModel):
    """General employee attributes."""
    user_name: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: str


class EmployeeCreate(EmployeeBase):
    """Employee attributes for registration."""
    model_config = ConfigDict(extra="forbid")
    password: str


class EmployeeOut(EmployeeBase):
    """Employee attributes for output."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str


class EmployeeInDB(EmployeeBase):
    id: int
    role: str
    hashed_password: str
