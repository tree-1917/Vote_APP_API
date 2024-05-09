from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
# Importing necessary modules and components from local files
from .. import schemas, database, models, oauth2

# Creating a router instance with a specified prefix and tags
router = APIRouter(
    prefix="/vote",
    tags=['Vote']  # Fixing the typo here from 'tages' to 'tags'
)

# POST endpoint for voting
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db)):
    # check post exist in table or not 
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    
    # Querying the database to find if the user has already voted on the post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                               models.Vote.user_id == 2)
    found_vote = vote_query.first()

    # Handling the case when the user wants to upvote
    if (vote.dir == 1):
        # Checking if the user has already voted on the post
        if found_vote:
            # Raising an exception if the user has already voted on the post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {2} has already voted on post {vote.post_id}")
        # Creating a new vote instance and adding it to the database
        new_vote = models.Vote(post_id=vote.post_id, user_id=2)
        db.add(new_vote)
        db.commit()
        # Returning a success message if the vote is added successfully
        return {"message": "successfully added vote"}
    # Handling the case when the user wants to remove the vote
    else:
        # Checking if the vote exists
        if not found_vote:
            # Raising an exception if the vote does not exist
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # Deleting the vote from the database
        vote_query.delete(synchronize_session=False)
        db.commit()
        # Returning a success message if the vote is deleted successfully
        return {"message": "successfully deleted vote"}
