from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from . import schema,models
import jwt




SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token,credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("userID")
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(id=str(id))
    except InvalidTokenError:
        raise credential_exception
    return token_data
   

def getCurrentUser(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        
    )
    token = verify_access_token(token,credential_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id)
    
    return user

