import os
import requests
import pandas as pd
import logging
import time

logger = logging.getLogger(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3"
REQUEST_TIMEOUT = 5  # seconds
MAX_RETRIES = 1

def enrich_recommendations(recommendations_df: pd.DataFrame):
    """
    Enriches a DataFrame of movie recommendations with data from TMDb.
    
    Args:
        recommendations_df: DataFrame with columns including 'tconst', 'primaryTitle', etc.
    
    Returns:
        List of dictionaries with enriched movie data
    """
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not found. Returning recommendations without enrichment.")
        # Return basic movie data without poster_url and overview
        return _convert_to_basic_format(recommendations_df)

    enriched_data = []
    
    for index, row in recommendations_df.iterrows():
        tconst = row['tconst']
        enriched_row = _get_basic_movie_data(row)
        
        # Try to enrich with TMDb data
        tmdb_data = _fetch_tmdb_data(tconst)
        if tmdb_data:
            enriched_row.update({
                "poster_url": tmdb_data.get('poster_url'),
                "overview": tmdb_data.get('overview')
            })
        else:
            # TMDb failed, but we still include the movie with null enrichment
            logger.debug(f"TMDb enrichment failed for {tconst}, including movie without poster/overview")
            enriched_row.update({
                "poster_url": None,
                "overview": None
            })
        
        enriched_data.append(enriched_row)
    
    return enriched_data

def _convert_to_basic_format(recommendations_df: pd.DataFrame):
    """Convert DataFrame to basic format when TMDb is not available"""
    basic_data = []
    for index, row in recommendations_df.iterrows():
        basic_row = _get_basic_movie_data(row)
        basic_row.update({
            "poster_url": None,
            "overview": None
        })
        basic_data.append(basic_row)
    
    return basic_data

def _get_basic_movie_data(row):
    """Extract basic movie data from DataFrame row"""
    return {
        "tconst": row['tconst'],
        "primaryTitle": row['primaryTitle'],
        "startYear": int(row['startYear']) if pd.notna(row['startYear']) else None,
        "genres": row['genres'],
        "averageRating": float(row['averageRating']) if pd.notna(row['averageRating']) else None,
    }

def _fetch_tmdb_data(tconst: str):
    """
    Fetch poster and overview from TMDb API using IMDb ID
    
    Args:
        tconst: IMDb ID (e.g., 'tt1234567')
    
    Returns:
        Dict with poster_url and overview, or None if failed
    """
    search_url = f"{TMDB_API_URL}/find/{tconst}?api_key={TMDB_API_KEY}&external_source=imdb_id"
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.get(search_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            data = response.json()
            
            # TMDb's find endpoint returns results in different lists
            if data.get('movie_results') and len(data['movie_results']) > 0:
                movie_info = data['movie_results'][0]
                poster_path = movie_info.get('poster_path')
                
                return {
                    "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
                    "overview": movie_info.get('overview')
                }
            
            # No movie results found
            logger.debug(f"No TMDb results found for {tconst}")
            return None
            
        except requests.exceptions.Timeout:
            logger.warning(f"TMDb API timeout for {tconst} (attempt {attempt + 1}/{MAX_RETRIES + 1})")
            if attempt < MAX_RETRIES:
                time.sleep(0.5)  # Brief delay before retry
                continue
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"TMDb API error for {tconst}: {str(e)}")
            if attempt < MAX_RETRIES:
                time.sleep(0.5)
                continue
            
        except Exception as e:
            logger.error(f"Unexpected error fetching TMDb data for {tconst}: {str(e)}")
            break
    
    return None
