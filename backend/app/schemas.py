import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- User Schemas ---

# This is the schema for data we expect when a user registers.
# The API will validate that the request body matches this shape.
class UserCreate(BaseModel):
    email: EmailStr  # Pydantic will validate this is a valid email format
    password: str

# This is the schema for the data we will send back as a response.
# Notice it does NOT include the password. We never send that back.
class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime
    
    # This Pydantic config tells SQLAlchemy how to read the data
    # from our ORM models (it's not a dict).
    class Config:
        from_attributes = True


# --- Token Schema ---

class Token(BaseModel):
    access_token: str
    token_type: str