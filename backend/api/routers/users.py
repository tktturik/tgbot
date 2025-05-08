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
from backend.api.routers.token import verify_temp_token
router = APIRouter()

@router.get("/get_users", response_model=List[Users])
async def get_users(
    _: dict = Depends(verify_temp_token),  
    db: Session = Depends(get_db)
    ):    
    users = db.query(User).all()
    return users