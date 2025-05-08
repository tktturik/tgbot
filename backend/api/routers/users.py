from fastapi import APIRouter, HTTPException, status
from jose import jwt, JWTError
from backend.schemas.user import Users
from fastapi.security import OAuth2PasswordBearer
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.db import get_db
from backend.models.user import User
from dotenv import load_dotenv
import os

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def verify_temp_token(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired temporary token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "token_id" not in payload:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


@router.get("/get_users", response_model=List[Users])
async def get_users(
    _: dict = Depends(verify_temp_token),  
    db: Session = Depends(get_db)
    ):    
    users = db.query(User).all()
    return users