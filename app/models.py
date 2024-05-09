# Import the Base class from the .database module
from .database import Base

# Import necessary components from the SQLAlchemy library
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
# Define a new class named Post, Which Create Posts Table in DB 
class Post(Base):
    # Define the name of the database table associated with the Post class
    __tablename__ = "posts"
    
    # Define the columns of the "posts" table
    
    # Define the id column as an integer primary key that cannot be null
    id = Column(Integer, primary_key=True, nullable=False)
    
    # Define the title column as a string that cannot be null
    title = Column(String, nullable=False)
    
    # Define the content column as a string that cannot be null
    content = Column(String, nullable=False)
    
    # Define the published column as a boolean with a default value of True
    published = Column(Boolean, server_default='TRUE',nullable=False)
    # Define the created_at Column as a TimeStamp 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # add foreign Key for tables     
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False )

    owner = relationship("User") # fetch data from Foreign Key Relationship and Return it 
    
# define a new class named User, Which Create a Users Table in DB.   
class User(Base) : 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)
class Vote(Base) : 
    __tablename__ = 'vote'
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True) 
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)


# Base class:
# The Base class is provided by SQLAlchemy and serves as the foundation for
# defining ORM models. It provides functionality for creating and managing
# database tables, as well as mapping Python classes to database tables.
# In this code, we inherit from the Base class to define our Post model,
# allowing SQLAlchemy to manage the mapping between the Post class
# and the "posts" table in the database.

