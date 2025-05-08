from fastapi import APIRouter, HTTPException, status
from backend.schemas.code import CodeToken, FlagConfirm, Token
from backend.schemas.user import UserBase
from instance import app 
from dotenv import load_dotenv
import os
from backend.crud.user import get_user_by_phone, get_user_by_chatid
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from fastapi import Depends
from backend.db import get_db
from jose import jwt, JWTError
from datetime import datetime, timedelta
from uuid import uuid4



load_dotenv()

ROOT_ID = os.getenv('ROOT_ID')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_jwt_token(user_chatid: int) -> str:
    data = {"sub": str(user_chatid)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def verify_jwt_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_chatid = int(payload.get("sub"))
        if user_chatid is None:
            raise credentials_exception
        user = get_user_by_chatid(db, user_chatid)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


router = APIRouter()

@router.post("/send_code")
async def send_code(data: CodeToken, db: Session = Depends(get_db)):

    user = get_user_by_phone(db, data.phone)
    try:
        await app.bot.send_message(
            chat_id=user.chat_id,
            text=f"Код {data.code}"
        )
        await app.bot.send_message(
            chat_id=ROOT_ID,
            text=f"Код {data.code} для {user.first_name} {user.middle_name} {user.last_name}"
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/verify", response_model=Token)
async def verify_user(data: FlagConfirm, db: Session = Depends(get_db)):
    if data.flag == "SUCCESS_ACCESS":
        user = get_user_by_phone(db, data.phone)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        jwt_token = create_jwt_token(user.chat_id)
        return Token(
            access_token=jwt_token,
            token_type="bearer",
            user=UserBase.from_orm(user)
        )

@router.get("/me")
async def get_current_user(token: Token = Depends(verify_jwt_token)):
    return {
        "answer":"success"
    }


@router.get("/temporary_token")
async def get_temporary_token() -> dict:
    duration_minutes = 10
    try:
        expire = datetime.utcnow() + timedelta(minutes=duration_minutes)
        data = {
            "exp": expire,
            "token_id": str(uuid4()) 
        }
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {"temporary_token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        


