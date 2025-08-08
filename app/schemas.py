from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

# Pydantic модели для задач и пользователей

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    name: str
    description: str | None = None 
    completed: bool = False

class TaskResponse(TaskCreate):
    id: int 
    created_at: datetime
    user_id: int
    owner: UserOut
    
    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None