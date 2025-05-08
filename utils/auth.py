from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud.user import get_user_by_chatid
from backend.db import SessionLocal

async def checkAuth(chat_id:int):
    db = SessionLocal()
    user = get_user_by_chatid(db, chat_id)

    if user:
        return user
    else:
        return None
