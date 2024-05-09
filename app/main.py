# === fastapi libs === #
from fastapi import FastAPI

# === routers 
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware
# # === local files
# from . import models  # import local models and schemas
# from .database import engine  # import database engine and session creation function

# Create database tables using SQLAlchemy ORM
# models.Base.metadata.create_all(bind=engine)

# Create a FastAPI application instance
app = FastAPI()

# Define allowed origins
origins = [
    "*"
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# == include routers == #  
app.include_router(post.router) # Post Routes
app.include_router(user.router) # User Routes
app.include_router(auth.router) # auth Routes
app.include_router(vote.router)
# Define root endpoint
@app.get('/')
async def root():
    # Return a welcome message
    return {"message" : "Welcome API"}
