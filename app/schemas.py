from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Incomming post structure using pydantic models
class Post(BaseModel):
    title: str
    published: bool = True
    content: str

    # owner_id:int #user id for collecting all the posts related to a user
    class Config:
        orm_mode = True


class BasicUserDetails(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


# Response structure using pydantic models, we can inherit Post class to make this
# more modular method since here we can add more features
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: BasicUserDetails
    class Config:
        orm_mode = True


class PutResponseTest(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime


# data for creating the user data that needs to be passed in
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# get every user details
class EveryUser(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime


# data going out of the response needs to keep this model
class UserOut(BaseModel):
    token: str
    tokenType: str

    class Config:
        orm_mode = True


# data model for token that is going out as response
class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData
class TokenData(BaseModel):
    id: Optional[int] = None


# data for login that is required. This function and usercreate function was replaced by fastapi.security.passwordForm
class Login(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
