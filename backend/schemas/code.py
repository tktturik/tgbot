from pydantic import BaseModel
from backend.schemas.user import UserBase

class CodeToken(BaseModel):
    phone: str
    code: str

class FlagConfirm(BaseModel):
    flag: str
    phone: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBase
