from sqlalchemy import create_engine  # Importing create_engine function to create SQLAlchemy Engine
from sqlalchemy.ext.declarative import declarative_base  # Importing declarative_base function to create base class for ORM models
from sqlalchemy.orm import sessionmaker  # Importing sessionmaker function to create Session class for database interactions
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database components from the environment variables
db_server = os.getenv("DB_SERVER")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"{db_server}://{db_user}:{db_password}@{db_host}/{db_name}"

# Create an SQLAlchemy Engine representing the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory (SessionLocal) that will produce individual Session instances
# It binds the session to the engine for database interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class (Base) for our ORM models using declarative_base function
Base = declarative_base()


# Dependency
def get_db():
    # Establish a new session for interacting with the database
    db = SessionLocal()
    try:
        # Yield the session to allow its use within a context manager
        yield db
    finally:
        # Close the session to release any resources it might be holding
        db.close()