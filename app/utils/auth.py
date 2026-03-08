"""Authentication and authorization utilities."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
import jwt
import os
from dotenv import load_dotenv

from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.security import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Employee:
    """
    Validate JWT token and retrieve the current user.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        Employee object if token is valid

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(sub=username)

    except InvalidTokenError:
        raise credentials_exception

    # Fetch user from database
    user = db.query(Employee).filter(
        Employee.username == token_data.sub
    ).first()

    if user is None:
        raise credentials_exception

    # Add is_admin property for easy access in routes
    user.is_admin = user.role == "admin"

    return user
