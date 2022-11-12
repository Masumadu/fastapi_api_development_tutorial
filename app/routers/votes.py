from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(tags=["Votes"], prefix="/votes")


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
        vote_data: schema.Vote,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote_data.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote_data.post_id} does not exist"
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote_data.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote_data.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post with id {vote_data.post_id}"
            )
        new_vote = models.Vote(post_id=vote_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote successfully added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote successfully deleted"}