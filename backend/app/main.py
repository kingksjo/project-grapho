
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .model_loader import load_model_assets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A dictionary to hold our loaded model assets
model_assets = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    logger.info("🚀 Application startup initiated...")
    try:
        logger.info("📥 Loading model assets...")
        assets = load_model_assets()
        model_assets.update(assets)
        logger.info(f"✅ Application startup completed. Loaded {len(assets)} model assets.")
    except Exception as e:
        logger.error(f"❌ Failed to load model assets during startup: {str(e)}")
        logger.warning("⚠️  Application will start but may have limited functionality.")
    
    yield
    
    # This code runs on shutdown
    logger.info("🛑 Application shutdown initiated...")
    model_assets.clear()
    logger.info("✅ Application shutdown completed.")

# Create the FastAPI app instance with the lifespan manager
app = FastAPI(
    title="Grapho Recommendation Engine API",
    description="A FastAPI-based recommendation engine for movies",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "message": "Recommender API is running!",
        "status": "healthy",
        "loaded_assets": list(model_assets.keys()) if model_assets else []
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_assets_loaded": len(model_assets),
        "available_assets": list(model_assets.keys()) if model_assets else []
    }

# You will add your other endpoints here later, for example:
# @app.get("/recommendations/{movie_id}")
# def get_recommendations(movie_id: str):
#     # Here you would use the assets from the model_assets dictionary
#     df = model_assets.get('movies_df')
#     # ... and so on
#     return {"message": f"Recommendations for {movie_id} would be here."}