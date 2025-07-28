import uuid
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    favorite_genres = Column(String, nullable=True)

# --- Movie Table ---
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    tconst = Column(String, nullable=False, unique=True, index=True) # Indexed for fast lookups
    primaryTitle = Column(String, nullable=False)
    startYear = Column(Integer, nullable=False)
    genres = Column(String, nullable=True)

# --- Interaction Table ---
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, nullable=False)
    # Define the foreign key relationship to the users table
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Define the foreign key relationship to the movies table
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    interaction_type = Column(String, nullable=False) # e.g., 'like', 'dislike'
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # These 'relationship' attributes are for the ORM. They help SQLAlchemy understand
    # how to join these tables and access related objects in our Python code.
    user = relationship("User")
    movie = relationship("Movie")