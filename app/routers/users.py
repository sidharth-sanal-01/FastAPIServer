from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",  # prefix will help in removing api heading lengths so basically if it is /posts/{id} u only need
    # to give /{id}
    tags=["users"],
)


# return every user
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.EveryUser])
def getAllUsers(db: Session = Depends(get_db)):
    print("Reached here")
    Users = db.query(models.Users).all()  # return all the data frm posts
    return Users


# to get user based on userId
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def getAlluser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    print(user)
    return user
