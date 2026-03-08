from pydantic import BaseModel
from app.schemas.employees import EmployeeOut


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None


class LoginResponse(BaseModel):
    employee: EmployeeOut
    access_token: str
    token_type: str
