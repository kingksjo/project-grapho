from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database 

# Create a new router object
router = APIRouter(
    prefix="/users", # All routes in this file will start with /users
    tags=["users"]    # Group these routes under "users" in the API docs
)

# Dependency to get a DB session (we can define it here or import it)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    # 1. Check if a user with this email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        # If the user exists, raise an HTTP 400 Bad Request error
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. If the user doesn't exist, call our CRUD function to create them
    new_user = crud.create_user(db=db, user=user)
    
    # FastAPI will handle serialization.
    return new_user