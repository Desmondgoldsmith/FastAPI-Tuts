from fastapi import Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema
from typing import List

router = APIRouter(
    tag = ['Auth']
)


@router.post('/login')
def LoginUser(db: Session = Depends(get_db)):
    
    return "something"