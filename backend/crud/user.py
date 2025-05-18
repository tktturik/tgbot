from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate
import random

def get_user_by_phone(db: Session, user_phone: str):
    return db.query(User).filter(User.phone_number == user_phone).first()

def get_user_by_chatid(db: Session, user_chat_id: int):
    return db.query(User).filter(User.chat_id == user_chat_id).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())  
    db.add(db_user)     
    db.commit()         
    db.refresh(db_user) 
    return db_user
def add_new_user(
    db: Session,
    phone_number: str,
    chat_id: int = random.randrange(0,100000),
    first_name: str = 'Новый',
    middle_name: str = 'Незарегистрированный',
    last_name: str = 'Пользователь',
    role: str = 'student',
    points: int = 0,
):
    user_data = UserCreate(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        phone_number=phone_number,
        chat_id=chat_id,
        role=role,
        points=points,
    )
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user