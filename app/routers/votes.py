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
    post = db.query(models.Post).filter(models.Post.id == votes.postId).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, details = "vote does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.postId == votes.postId, models.Votes.userId == current_user.userId)
    found_vote_data = vote_query.first()
    
    if(votes.action == 1):
        if found_vote_data:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, details = "you have already voted. ypu cannot vote again!")
        new_vote = models.Votes(postId == votes.postId, userId == current_user.userId)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, details = "Cannot find vote!")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "Vote deleted successfully"}

        
        

            
            
