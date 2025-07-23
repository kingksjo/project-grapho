from passlib.context import CryptContext

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