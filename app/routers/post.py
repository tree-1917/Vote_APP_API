# Importing necessary modules and functions
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas,oauth2
from ..database import get_db

# Create a router instance
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Route to retrieve all posts
# @router.get("/", response_model=List[schemas.Post])
@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    # Retrieve all posts from the database
    posts = db.query(models.Post).all() # return all posts for all users 
    
    # Execute the query to retrieve Post objects and their corresponding vote counts
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                .group_by(models.Post.id) \
                .all()

    # Construct a list of dictionaries with the required data
    formatted_results = [{"post": post.__dict__, "votes": votes} for post, votes in results]

    # Return the formatted results
    return formatted_results


# Route to retrieve a post by its ID 
# @router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}")
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    try:
        # Query the database for the post with the given ID and its vote count
        post_with_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                       .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
                       .group_by(models.Post.id) \
                       .filter(models.Post.id == id) \
                       .first()

        if not post_with_votes:
            # If the post with the given ID does not exist, raise an HTTP exception
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Post with id {id} was not found.'
            )

        # Extract the post and vote count from the query result tuple
        post, votes = post_with_votes

        # Construct a dictionary containing the post details and vote count
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "votes": votes
        }

        return post_data
    except Exception as e:
        # If an unexpected exception occurs, return an internal server error
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal Server Error", 'detail': str(e)}    

# Route to create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Create a new Post object based on the request data
    
    new_post = models.Post(**post.dict(),owner_id=2) 
    # Add the new post to the database
    db.add(new_post)
    # Save changes to the database
    db.commit()
    # Refresh the object to get any database-generated values
    db.refresh(new_post)
    return new_post

# Route to delete a post by its ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # Query the database for the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        # If the post with the given ID does not exist, raise an HTTP exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exists .")
    # check if owner who try to delete it's post 
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # Delete the post from the database
    post_query.delete(synchronize_session=False)
    # Save changes to the database
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a post by its ID 
@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Query the database for the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if my_post is None:
        # If the post with the given ID does not exist, raise an HTTP exception
        raise HTTPException(status_code=404, detail=f"post with id {id} does not exists .")
    # check if owner try change his post 
    if  my_post.owner_id != current_user.id : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    # Update the post with the new data
    post_query.update(post.dict(), synchronize_session=False)
    # Save changes to the database
    db.commit()

    return post_query.first()
