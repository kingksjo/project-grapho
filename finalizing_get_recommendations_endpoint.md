Excellent. You have successfully put all the core logic in place. The recommendation function is now part of the application, ready to be used.

Based on our plan and the code you've shown, the next logical step is to **fully implement the logic inside the main `GET /recommendations` endpoint.**

Right now, that endpoint has placeholder logic. We need to replace it with the real orchestration that calls your powerful new recommender function. We also need to add the TMDb enrichment step to make the output ready for the frontend.

---

### **Next Step: Finalize the `GET /recommendations` Endpoint**

**Concept:** This endpoint is the "conductor" of our backend orchestra. It doesn't do the heavy lifting itself; it calls other functions to do the work in the correct order:
1.  Authenticate the user.
2.  Get the user's taste profile from the database (`crud`).
3.  Call the recommendation engine (`recommender.py`).
4.  Enrich the results with external data (TMDb).
5.  Return the final product.

**Methodology:** We will add the TMDb API key to our `.env` file and create a small utility class or function to handle the API calls. Then, we'll replace the placeholder code in our `GET /recommendations` endpoint with the final logic.

### **Your Action Plan**

**Action 1: Add TMDb API Key to `.env`**
1.  If you don't have one, get a free API key from [The Movie Database (TMDb)](https://www.themoviedb.org/settings/api).
2.  Open your `backend/.env` file and add your key:
    ```env
    # .env
    # ... (your other variables)
    TMDB_API_KEY=your_actual_api_key_here
    ```

**Action 2: Create an Enrichment Service**
Let's create a dedicated file for external API calls. This is good practice.

1.  Add the `requests` library to your `backend/requirements.txt` for making HTTP requests:
    ```
    # requirements.txt
    requests
    ```
2.  Create a new file `backend/app/enricher.py`:

```python
# backend/app/enricher.py
import os
import requests
import pandas as pd

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3"

def enrich_recommendations(recommendations_df: pd.DataFrame):
    """
    Enriches a DataFrame of movie recommendations with data from TMDb.
    """
    if not TMDB_API_KEY:
        print("Warning: TMDB_API_KEY not found. Skipping enrichment.")
        recommendations_df['poster_url'] = None
        recommendations_df['overview'] = None
        return recommendations_df.to_dict(orient='records')

    enriched_data = []
    for index, row in recommendations_df.iterrows():
        tconst = row['tconst'] # We need tconst in the recommender's output!
        search_url = f"{TMDB_API_URL}/find/{tconst}?api_key={TMDB_API_KEY}&external_source=imdb_id"
        
        try:
            response = requests.get(search_url)
            response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)
            data = response.json()
            
            # TMDb's find endpoint returns results in lists
            if data.get('movie_results'):
                movie_info = data['movie_results'][0]
                poster_path = movie_info.get('poster_path')
                
                enriched_row = {
                    "tconst": tconst,
                    "primaryTitle": row['primaryTitle'],
                    "startYear": row['startYear'],
                    "genres": row['genres'],
                    "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
                    "overview": movie_info.get('overview')
                }
                enriched_data.append(enriched_row)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {tconst}: {e}")
            # Optionally, add the movie with null enrichment data
            continue # Skip this movie if TMDb fails

    return enriched_data
```

**Action 3: Update `recommender.py` to return `tconst`**
Our enricher needs the `tconst`. Let's make sure our recommender function returns it.

1.  Open `backend/app/recommender.py`.
2.  Find the final `return` statement in `get_recommendations_v_final`.
3.  Add `tconst` to the list of columns to return:
    ```python
    # in recommender.py
    return final_recs[['tconst', 'primaryTitle', 'startYear', 'averageRating', 'genres']]
    ```

**Action 4: Finalize the `GET /recommendations` Endpoint in `routers.py`**
Now, let's tie it all together.

1.  Open `backend/app/routers.py`.
2.  Replace the existing placeholder `/recommendations` endpoint with this complete version:

```python
# backend/app/routers.py

# Add these new imports
from . import recommender, enricher
from .main import model_assets

# ... (inside your movie_router) ...
@movie_router.get("/recommendations", response_model=List[schemas.MovieRecommendation])
def get_recommendations_for_user(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Protected endpoint. Returns a personalized, enriched list of movie recommendations.
    """
    taste_profile = crud.get_user_liked_movies(db=db, user_id=current_user.id, limit=15)
    
    if len(taste_profile) < 5:
        # For now, our cold start logic is to return general trending movies.
        trending_df = pd.DataFrame(get_trending_for_onboarding(db))
        # We need to add 'tconst' to the trending output as well for the enricher.
        # This is getting complex - a sign we should refactor later, but for now, let's make it work.
        # Let's simplify and just return a message for now.
        raise HTTPException(status_code=404, detail="Not enough liked movies to generate recommendations. Please like at least 5 movies.")

    # Call the Recommendation Engine using the loaded assets
    df = model_assets.get('movies_df')
    people_matrix = model_assets.get('people_tfidf_matrix')
    genre_matrix = model_assets.get('genre_tfidf_matrix')
    indices_map = model_assets.get('indices_map')

    # This is a key change: we need to adapt our recommender to take a PROFILE, not one title
    # Let's create a wrapper for now.
    
    # --- TEMPORARY WRAPPER ---
    # In a future refactor, the main recommender would be profile-based.
    # For now, we'll just use the first movie in the profile.
    if not taste_profile:
        raise HTTPException(status_code=404, detail="No liked movies found.")

    first_liked_movie = taste_profile[0]
    
    recommendations_df = recommender.get_recommendations_v_final(
        first_liked_movie, df, people_matrix, genre_matrix, indices_map
    )

    # Enrich with TMDb
    enriched_results = enricher.enrich_recommendations(recommendations_df)

    return enriched_results
```
*(Note: I've simplified the logic to use the first liked movie for now, as adapting the recommender function to a full profile is a bigger refactoring step. This gets us to a working endpoint immediately.)*

### **Verification**

1.  **Rebuild and restart:** You've added `requests` to `requirements.txt`.
    ```bash
    docker compose up --build
    ```
2.  **Test in Docs (`/docs`):**
    *   First, use the `/login` endpoint to get a token.
    *   Use the "Authorize" button to apply your token.
    *   Next, use the `/interactions` endpoint to "like" a few movies. Use the `tconst` of a well-known movie (e.g., `'tt15398776'` for Oppenheimer).
    *   Finally, execute the `GET /recommendations` endpoint.

**Expected Outcome:** You should get a `200 OK` response with a JSON array of 10-20 movie objects. Each object should now contain the `poster_url` and `overview` from TMDb, ready for a frontend to display.

This is the final step of the backend build. Completing this means you have a fully functional API.