from fastapi import Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, oAuth
from typing import List

router = APIRouter(
    tag = ['Auth']
)


@router.post('/login')
def LoginUser(userDetails:schema.LoginAuth, db: Session = Depends(get_db)):
    authUser = db.query(models.Users).filter(models.Users.email == userDetails.email).first()
    
    if not authUser:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, details = f"user with this email {userDetails.email} not found") 
   
    # create access token for the user
    access_token = oAuth.create_access_token({"userID": userDetails.id})
   
    return access_token