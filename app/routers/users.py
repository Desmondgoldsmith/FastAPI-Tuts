from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, utils
from typing import List


# initializing the router
router = APIRouter(
    # set the title of the section rendering the Users api details on the Api docs page to Users
    tag = ['Users']
)

# add a user
@router.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=schema.UsersResponse)
def addUser(users:schema.UserSchema, db: Session = Depends(get_db)):
    # hash user password
    password_hash = utils.Hash(users.password)
    users.password = password_hash
    
    user_data = models.Users(**users.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


# get user
@router.get('/user/{id}', response_model= schema.UsersResponse)
def getUser(id:int, db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    return user
