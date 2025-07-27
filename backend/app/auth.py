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