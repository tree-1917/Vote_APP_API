from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional
# === User Out === # 
class UserOut(BaseModel) :
    id : int 
    email : EmailStr

    class Config : 
        from_attributes = True 
# === Request === #  
# make a schema for user input 
class PostBase(BaseModel) : 
    title : str 
    content : str 
    class Config : 
        from_attributes = True 

    

class PostCreate(PostBase) : 
    pass 

# === Response === # 
class Post(PostBase) : 
    id : int
    owner_id : int  
    owner : UserOut
    # make ORM know Pydantic Model
    class Config:
        # orm_mode => from_attributes
        from_attributes = True 

class PostOut(PostBase) :
    Post : Post 
    votes: int
    class Config:
        # orm_mode => from_attributes
        from_attributes = True 
# === User === # 
class UserCreate(BaseModel) : 
    email : EmailStr
    password : str
    


# === user login === # 
class UserLogin(BaseModel) : 
    email : EmailStr
    password : str
    
    
# === Access Token === #

class Token(BaseModel) : 
    access_token : str
    token_type : str 
    
class TokenData(BaseModel) : 
    id : Optional[str] = None
    
# === vote 

class Vote(BaseModel) : 
    post_id : int 
    dir : conint(le=1)

