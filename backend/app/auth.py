from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# 1. Create a CryptContext instance
#    This tells passlib which hashing algorithm to use.
#    "bcrypt" is the recommended standard.
#    'deprecated="auto"' will automatically handle updating hashes if we ever change the algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 2. Function to hash a password
def hash_password(password: str):
    """
    Takes a plain-text password and returns its bcrypt hash.
    """
    return pwd_context.hash(password)


# 3. Function to verify a password
def verify_password(plain_password: str, hashed_password: str):
    """
    Compares a plain-text password with a stored hash.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# 4. Function to create a JWT access token
def create_access_token(data: dict):
    """
    Creates a new JWT access token.
    
    Args:
        data (dict): The payload to include in the token.
    
    Returns:
        str: The encoded JWT string.
    """
    to_encode = data.copy()
    
    # Set the token's expiration time
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Create JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def verify_access_token(token: str, credentials_exception):
    """
    Decodes the JWT to get the user_id from the payload.
    """
    try:
        # Decode the JWT using our secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the user_id from the payload
        user_id: str = payload.get("user_id")

        if user_id is None:
            # If there is no user_id in the token, raise an error
            raise credentials_exception
        
        # We can create a Pydantic schema for the token data if we want
        # For now, just returning the user_id is fine.
        return user_id
    
    except JWTError:
        # If the token is invalid (bad signature, expired, etc.), raise an error
        raise credentials_exception


# --- NEW: The Main "Get Current User" Dependency ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    A dependency that can be used in any protected endpoint.
    It verifies the token and returns the full user object from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify the token to get the user's ID
    user_id = verify_access_token(token, credentials_exception)
    
    # Get the user from the database using the ID from the token
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # You could add more checks here, e.g., if user.is_active is False
    
    return user