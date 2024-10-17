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
    vote_query = db.query(models.Votes.postId).filter(models.Votes.postId == votes.postId, models.Votes.userId == current_user.userId)
    vote_data = vote_query.first()
    
    if(votes.action == 1):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, details = "you have already voted. ypu cannot vote again!")
    
    new_vote = models.Votes(postId == votes.postId, userId == current_user.userId)
    db.add()
    db.commit()
    return {"message": "Vote added successfully"}
    else:
        if(votes.action == 0):
            
