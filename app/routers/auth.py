from fastapi import Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oAuth, schema
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router = APIRouter(
    tags = ['Auth']
)


@router.post('/login', response_model= schema.Token)
def LoginUser(userDetails:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    authUser = db.query(models.Users).filter(models.Users.email == userDetails.username).first()
    
    if not authUser:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, details = f"user with this email {userDetails.username} not found") 
   
    if not utils.verify_password(userDetails.password,authUser.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, details = f"wrong user password")
   
    # create access token for the user
    access_token = oAuth.create_access_token(data = {"userID": authUser.id})
   
    return {"token":access_token, "type": "bearer"}