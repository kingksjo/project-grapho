
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .model_loader import load_model_assets

# A dictionary to hold our loaded model assets
model_assets = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    print("Application startup...")
    assets = load_model_assets()
    model_assets.update(assets)
    yield
    # This code runs on shutdown
    print("Application shutdown...")
    model_assets.clear()

# Create the FastAPI app instance with the lifespan manager
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Recommender API is running!"}

# You will add your other endpoints here later, for example:
# @app.get("/recommendations/{movie_id}")
# def get_recommendations(movie_id: str):
#     # Here you would use the assets from the model_assets dictionary
#     df = model_assets.get('movies_df')
#     # ... and so on
#     return {"message": f"Recommendations for {movie_id} would be here."}