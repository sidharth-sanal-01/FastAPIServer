from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

#whatever login endpoing we are keeping we need to add that
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key
secret_key = "0679485bce8238c122a0d842637c98f60bfba0619a475ded6a2aea13398c7f4a"

# Algorithm
algorithm = "HS256"

# expiration time
access_token_expiration = 10


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=access_token_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt


def verify_acceess_token(token: str, credentialsException):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        id: str = payload.get("userId")
        if id is None:
            raise credentialsException
    except JWTError:
        print("Token Error")
        raise credentialsException


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_acceess_token(token, credentials_exception)
