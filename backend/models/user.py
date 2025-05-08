from sqlalchemy import Column, Integer, String
from backend.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    phone_number = Column(String(20), unique=True, nullable=False)
    chat_id = Column(Integer, unique=True)
    points = Column(Integer, default=0)
    role = Column(String(20), nullable=False, default='student')