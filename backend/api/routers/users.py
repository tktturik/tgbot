from fastapi import APIRouter
from backend.schemas.user import Users

from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.db import get_db
from backend.models.user import User

router = APIRouter()

@router.get("/get_users", response_model=List[Users])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users