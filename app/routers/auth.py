from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils
from .. import oauth2

# setup a route for user login
router = APIRouter(tags=["Authentication"])


# for a use to login we use this route this will return a jwt token
@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(
    userCredentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # searching for user in database
    searchUser = (
        db.query(models.Users)
        .filter(models.Users.email == userCredentials.username)
        .first()
    )

    # returning error is username is wrong
    if searchUser == None:
        raise HTTPException(
            detai="User not found..Please signup and create an account..",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # returning error if username is correct and password is wrong
    if not utils.verifyPassword(searchUser.password, userCredentials.password):
        raise HTTPException(
            detail="User Password wrong..Please try again...",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # creating a token
    token = oauth2.create_access_token(data={"userId": searchUser.id})
    return {"access_token": token, "token_type": "bearer"}


# create a user
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(userCredentials.password)
    userCredentials.password = hashed_password
    newUser = models.Users(**userCredentials.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

