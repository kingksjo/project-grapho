import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

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

# Schema for updating a user's favorite genres during onboarding.
class UserUpdateGenres(BaseModel):
    # Expects a JSON object like: {"genres": ["Action", "Drama", "Sci-Fi"]}
    genres: List[str]

# Schema for creating a new user interaction (like/dislike).
class InteractionCreate(BaseModel):
    # Expects a JSON object like: {"tconst": "tt15398776", "interaction_type": "like"}
    tconst: str
    interaction_type: str

# Schema for the final recommendation object we send to the frontend.
#    This includes the enriched data from TMDb.
class MovieRecommendation(BaseModel):
    tconst: str
    primaryTitle: str
    startYear: int
    genres: Optional[str] = None # Make genres optional in case some movies don't have them
    poster_url: Optional[str] = None # This will come from TMDb
    overview: Optional[str] = None   # This will come from TMDb
    
    # This config allows Pydantic to create this schema from an ORM object
    class Config:
        from_attributes = True

