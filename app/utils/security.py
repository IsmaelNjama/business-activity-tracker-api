from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,  HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.employees import EmployeeOut
from app.schemas.security import TokenData


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


password_hash = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    if not plain_password:
        raise ValueError("Password cannot be empty")
    return password_hash.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


#  utility function to generate a new access token.
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
