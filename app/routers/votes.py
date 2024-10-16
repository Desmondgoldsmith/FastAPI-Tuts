from fastapi import Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, oAuth
from typing import List

router = APIRouter(
    prefix = "/votes"
    tags = ['Votes']
)


@router.post('/')
def addVotes(votes = schema.VotesData, db:Session = Depends('get_db'), current_user = Depends(oAuth.getCurrentUser)):
    return {"message": "Vote added successfully"}