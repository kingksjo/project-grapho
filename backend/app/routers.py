from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database 
from fastapi.security import OAuth2PasswordRequestForm
from . import auth

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

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint for user login. Returns a JWT access token.
    """
    # 1. Authenticate the user
    user = crud.get_user_by_email(db, email=form_data.username) # The form uses 'username' for the email field
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Create the access token
    #    The payload for the token will contain the user's ID.
    access_token = auth.create_access_token(
        data={"user_id": str(user.id)} # Convert UUID to string for JSON compatibility
    )
    
    # 3. Return the token
    return {"access_token": access_token, "token_type": "bearer"}