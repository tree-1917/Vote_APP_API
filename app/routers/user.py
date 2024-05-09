# Importing necessary modules and functions
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,utils
from ..database import get_db

# Create a router instance
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Route to add a user to the database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before storing it in the database
    user.password = utils._hash(user.password)
    # Create a new user object
    new_user = models.User(**user.dict())
    # Add the new user to the database
    db.add(new_user)
    # Commit the transaction
    db.commit()
    # Refresh the object to get any database-generated values
    db.refresh(new_user)
    return new_user

# Route to get data about a user by their ID
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # Query the database for the user with the given ID
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # If the user with the given ID does not exist, raise an HTTP exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user
