import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")

# The hostname 'db' is the service name we defined in our docker-compose.yml
DB_HOST = "db" 
DB_PORT = "5432"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of the SessionLocal class will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class that our ORM models will inherit from.
Base = declarative_base()

# Dependency to get a DB session (we can define it here or import it)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()