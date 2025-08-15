import logging
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text
from .model_loader import load_model_assets
from . import models, database, seed_db, assets
from .routers import router as user_router, movie_router
import typer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    logger.info("Application startup initiated...")
    try:
        logger.info("Loading model assets...")
        loaded_assets = load_model_assets()
        assets.update_model_assets(loaded_assets)
        logger.info(f"Application startup completed. Loaded {len(loaded_assets)} model assets.")
        
        
        
    except Exception as e:
        logger.error(f"Failed to load model assets during startup: {str(e)}")
        logger.warning(" Application will start but may have limited functionality.")
    
    yield
    
    # This code runs on shutdown
    logger.info("Application shutdown initiated...")
    assets.clear_model_assets()
    logger.info("Application shutdown completed.")


cli_app = typer.Typer()

# Create the FastAPI app instance with the lifespan manager
app = FastAPI(
    title="Grapho Recommendation Engine API",
    description="A FastAPI-based recommendation engine for movies",
    version="1.0.0",
    lifespan=lifespan
)

# Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include the routers
app.include_router(user_router)
app.include_router(movie_router)

@app.get("/db-check")
def database_check(db: Session = Depends(get_db)):
    """
    A simple endpoint to verify the database connection.
    """
    try:
        # Perform a simple, fast, read-only query.
        # This query asks the database for its current version.
        result = db.execute(text("SELECT 1"))
        if result.scalar_one() == 1:
            logger.info("Database connection verified successfully")
            return {"status": "ok", "message": "Database connection successful!"}
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        # If anything goes wrong, raise an HTTP exception.
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@app.get("/")
def read_root():
    model_assets = assets.get_model_assets()
    return {
        "message": "Recommender API is running!",
        "status": "healthy",
        "loaded_assets": list(model_assets.keys()) if model_assets else []
    }

@app.get("/health")
def health_check():
    model_assets = assets.get_model_assets()
    return {
        "status": "healthy",
        "model_assets_loaded": len(model_assets),
        "available_assets": list(model_assets.keys()) if model_assets else []
    }


@cli_app.command("seed-db-command")
def seed_db_command():
    """
    Command-line utility to seed the database with movie data.
    """
    typer.echo("Seeding process initiated...")
    
    # We can't use the 'model_assets' from the running app,
    # so we'll load them fresh for this one-off command.
    assets = load_model_assets()
    movies_df = assets.get('movies_df')
    
    if movies_df is not None:
        db = database.SessionLocal()
        try:
            # Call our refactored seeder function
            seed_db.seed_movies_table(db, movies_df)
        finally:
            db.close()
    else:
        typer.echo("Could not load movies_df. Aborting.")


if __name__ == "__main__":
    cli_app()
# You will add your other endpoints here later, for example:
# @app.get("/recommendations/{movie_id}")
# def get_recommendations(movie_id: str):
#     # Here you would use the assets from the model_assets dictionary
#     df = model_assets.get('movies_df')
#     # ... and so on
#     return {"message": f"Recommendations for {movie_id} would be here."}