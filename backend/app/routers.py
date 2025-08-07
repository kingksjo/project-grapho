from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging
import pandas as pd
from . import crud, schemas, database, models
from fastapi.security import OAuth2PasswordRequestForm
from . import auth, recommender, enricher, assets

logger = logging.getLogger(__name__)

# Create a new router object
router = APIRouter(
    prefix="/users", # All routes in this file will start with /users
    tags=["users"]    # Group these routes under "users" in the API docs
)

movie_router = APIRouter(
    tags=["movies"] # Group these under "movies" in the API docs
)



@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
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

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """
    A protected endpoint that returns the information for the currently logged-in user.
    """
    # The 'current_user' is provided by the get_current_user dependency.
    # If the request gets this far, the user is authenticated.
    # We can just return the user object, and FastAPI will serialize it.
    return current_user


# Movie-related routes 

@movie_router.get("/onboarding/trending", response_model=List[schemas.MovieRecommendation])
def get_trending_for_onboarding(db: Session = Depends(database.get_db)):
    """
    Returns a list of popular movies/shows from the last 3 years for the onboarding process.
    """
    three_years_ago = datetime.now().year - 3
    
    trending_movies = db.query(models.Movie).filter(
        models.Movie.startYear >= three_years_ago
    ).order_by(
        models.Movie.numVotes.desc() # We need to add numVotes to our model first!
    ).limit(50).all()

    # We use our MovieRecommendation schema, but poster_url and overview will be None
    # The frontend can fetch these if needed, or we can enrich them here.
    # For now, this is efficient.
    return trending_movies

@router.post("/me/genres", response_model=schemas.UserResponse)
def update_genres_for_user(
    genres_update: schemas.UserUpdateGenres,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Protected endpoint to update the favorite genres for the current user.
    """
    return crud.update_user_genres(db=db, user_id=current_user.id, genres=genres_update)


# --- Endpoint 3: Handle Interactions (can be in a new interactions_router or movie_router) ---
@movie_router.post("/interactions", status_code=201)
def create_interaction(
    interaction: schemas.InteractionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Protected endpoint to save a user's interaction (like/dislike) with a movie.
    """
    return crud.create_or_update_interaction(db=db, user_id=current_user.id, interaction=interaction)


# --- Endpoint 4: The Main Recommendation Endpoint ---
@movie_router.get("/recommendations", response_model=List[schemas.MovieRecommendation])
def get_recommendations_for_user(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Protected endpoint. Returns a personalized, enriched list of movie recommendations.
    """
    # 1. Get user's taste profile
    taste_profile = crud.get_user_liked_movies(db=db, user_id=current_user.id, limit=15)
    
    # 2. Handle insufficient data
    if not taste_profile:
        raise HTTPException(
            status_code=404, 
            detail="No liked movies found. Please like some movies first using the /interactions endpoint."
        )
    
    # 3. Load model assets
    model_assets = assets.get_model_assets()
    df = model_assets.get('movies_df')
    people_matrix = model_assets.get('people_tfidf_matrix')
    genre_matrix = model_assets.get('genre_tfidf_matrix')
    indices_map = model_assets.get('indices_map')
    
    # Check if all required assets are loaded
    if not all([df is not None, people_matrix is not None, genre_matrix is not None, indices_map is not None]):
        raise HTTPException(
            status_code=500,
            detail="Model assets not properly loaded. Please check server logs."
        )
    
    # 4. Generate recommendations using the recommendation engine
    try:
        recommendations_df = recommender.get_recommendations_v_final(
            liked_movies_profile=taste_profile,
            df=df,
            people_matrix=people_matrix,
            genre_matrix=genre_matrix,
            indices_map=indices_map
        )
        
        if recommendations_df.empty:
            # Fallback to trending movies if recommendation engine returns empty
            logger.warning(f"Recommendation engine returned no results for user {current_user.id}, falling back to trending")
            return get_trending_for_onboarding(db)
            
    except Exception as e:
        logger.error(f"Recommendation engine failed for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate recommendations. Please try again later."
        )
    
    # 5. Enrich with TMDb data
    try:
        enriched_recommendations = enricher.enrich_recommendations(recommendations_df)
        return enriched_recommendations
        
    except Exception as e:
        logger.error(f"TMDb enrichment failed for user {current_user.id}: {str(e)}")
        # Return basic recommendations without enrichment as fallback
        basic_recommendations = []
        for _, row in recommendations_df.iterrows():
            basic_recommendations.append({
                "tconst": row['tconst'],
                "primaryTitle": row['primaryTitle'],
                "startYear": int(row['startYear']) if pd.notna(row['startYear']) else None,
                "genres": row['genres'],
                "averageRating": float(row['averageRating']) if pd.notna(row['averageRating']) else None,
                "poster_url": None,
                "overview": None
            })
        return basic_recommendations