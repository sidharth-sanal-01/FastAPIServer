from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from fastapi.params import Body
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils

router=APIRouter(
    prefix="/users", #prefix will help in removing api heading lengths so basically if it is /posts/{id} u only need 
    #to give /{id}
    tags=["users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #hash the password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    newUser=models.Users(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.UserOut])
def getAllUsers(db:Session=Depends(get_db)):
    Users=db.query(models.Users).all() #return all the data frm posts
    return Users

@router.post("/login",status_code=status.HTTP_200_OK)
def login(user:schemas.Login,db:Session=Depends(get_db)):
    # post=db.query(models.Post).filter(models.Post.id==id).first() #using the filter method to filter based on ID and first method to return first match
    userLogin=db.query(models.Users).filter(models.Users.email==user.email).first()
    #checking if user is present in our db
    if userLogin==None:
        #user is not present and we are raising error of User not Found
        raise HTTPException(detail="User Not Found",status_code=status.HTTP_401_UNAUTHORIZED)
    
    #if user is present in our db , we have to check password
    hashed_password=utils.hash(user.password)
    print(hashed_password,":",userLogin.password)
    if userLogin.password!=hashed_password:
        raise HTTPException(detail="Wrong Password....Please try again",status_code=status.HTTP_401_UNAUTHORIZED)
    
    #returning the password if login is correct
    return userLogin

#to get user based on userId
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def getAlluser(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    print(user)
    return user

    
