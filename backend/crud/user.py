from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate

def get_user_by_phone(db: Session, user_phone: str):
    return db.query(User).filter(User.phone_number == user_phone).first()

def get_user_by_chatid(db: Session, user_chat_id: int):
    return db.query(User).filter(User.chat_id == user_chat_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())  
    db.add(db_user)     
    db.commit()         
    db.refresh(db_user) 
    return db_user