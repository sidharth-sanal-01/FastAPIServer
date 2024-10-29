from pydantic import BaseModel, EmailStr
from datetime import datetime


# Incomming post structure using pydantic models
class Post(BaseModel):
    title: str
    published: bool = True
    content: str


# Response structure using pydantic models, we can inherit Post class to make this
# more modular method since here we can add more features
class Response(Post):
    # id:int
    created_at: datetime

    class Config:
        orm_mode = True

#
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    token: str
    tokenType: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str

class Login(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
