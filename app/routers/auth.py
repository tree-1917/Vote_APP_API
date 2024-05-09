from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token  )
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Endpoint to authenticate users and generate access tokens.
    
    :param user_credentials: OAuth2PasswordRequestForm containing username and password.
    :param db: SQLAlchemy Session.
    :return: Dictionary containing access token and token type.
    """
    # Retrieve user from the database based on the provided email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() 
    
    # Verify if the user exists
    if not user : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # Verify the password using the utility function _verify
    if not utils._verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # Return the token
    return {"access_token" : access_token, "token_type" : "bearer"}
