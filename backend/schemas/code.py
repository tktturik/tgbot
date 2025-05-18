from pydantic import BaseModel
from backend.schemas.user import UserBase

class CodeToken(BaseModel):
    id: int
    code: str

class FlagConfirm(BaseModel):
    flag: str
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBase
