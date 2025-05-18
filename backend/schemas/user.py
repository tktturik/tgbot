from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone_number: str
    chat_id: int
    role: str
    points: int
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    first_name: str = 'Новый'
    middle_name: str = 'Незарегистрированный'
    last_name: str = 'Пользователь'
    phone_number: str
    chat_id: int
    points: int = 0
    role: str = 'student'

class Users(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    id: int

class User(UserBase):
    id: int
    points: int
    role: str
    
    class Config:
        from_attributes = True