from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Load environment variables from .env file
load_dotenv()

# Get the values of the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Function to create an access token for the user
def create_access_token(data: dict):
    print(data)
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt

# Define a function named verify_access_token that takes a token string and a credentials_exception object as arguments
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the token using the secret key and specified algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Print the decoded payload (optional)
        print(payload)

        # Extract user ID from the payload
        user_id: str = payload.get("user_id")

        # If user ID is not present in the payload, raise credentials_exception
        if user_id is None:
            raise credentials_exception

        # Create a TokenData object with the extracted user ID
        token_data = schemas.TokenData(id=user_id)

    # If any JWTError occurs during decoding, raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Return the extracted token data
    return token_data


# Define a function named get_current_user that takes a token string and a database session as arguments
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Define an HTTPException object to be raised if credentials are not validated
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # Verify the access token using the verify_access_token function
    token = verify_access_token(token, credentials_exception)

    # Query the database to get the user corresponding to the extracted user ID from the token
    user = db.query(models.User).filter(models.User.id == token.id).first()

    # Return the user
    return user
