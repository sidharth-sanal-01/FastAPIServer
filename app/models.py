from .database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

#post model for creating postgres database, This does not have any connection with pydanitc model
#This will create a table if it does not exist and get the existing one if it is there
class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True, nullable=False)
    title =Column(String, nullable=False)
    content= Column(String, nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


