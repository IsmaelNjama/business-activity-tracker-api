from pydantic import BaseModel, EmailStr, ConfigDict, Field


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


class EmployeeOut(EmployeeBase):
    """Employee attributes for output."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    role: str


class EmployeeInDB(EmployeeBase):
    id: int
    role: str
    hashed_password: str
