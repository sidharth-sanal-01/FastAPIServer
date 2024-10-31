from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas,database,models

"""
whatever login endpoind we are keeping we need to add that
This line makes the fastapi look for a bearer token inside the
authorization header - If the authorization header is present
outhscheme ie the Oauth2PasswordBearer retireves the token
and gives it to the token variable in the function

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key
secret_key = "0679485bce8238c122a0d842637c98f60bfba0619a475ded6a2aea13398c7f4a"

# Algorithm
algorithm = "HS256"

# expiration time
access_token_expiration = 60    

"""
This function will create an access token by taking the time given 
and details provided with an expiration date and signature.
After the expiration this token should not work
"""
def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt

"""
The jwt.decode function automatically checks the time inside
the token for which it is set to be expired and if the current
time is greater than that it will raise a JWTerror since token
is expired..

"""
def verify_acceess_token(token: str, credentialsException):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        id: int = payload.get("userId")
        if id is None:
            raise credentialsException
        token=schemas.TokenData(id=id)
    except JWTError:
        print("Token Error")
        raise credentialsException
    
    return token

# Here oauth2_scheme is very important since it helps
# in collecting the token details from authorization header  
async def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    verified_token=verify_acceess_token(token,credentials_exception)
    # #getting the current user
    user=db.query(models.Users).filter(models.Users.id==verified_token.id).first() 
    return user
