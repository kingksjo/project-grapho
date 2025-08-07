import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

def get_recommendations_v_final(liked_movies_profile, df, people_matrix, genre_matrix, indices_map):
    """
    Generate recommendations based on a profile of liked movies.
    
    Args:
        liked_movies_profile: List of movie titles in 'Title (Year)' format
        df: Movies DataFrame
        people_matrix: People TF-IDF matrix
        genre_matrix: Genre TF-IDF matrix
        indices_map: Mapping from 'Title (Year)' to DataFrame indices
    
    Returns:
        DataFrame with recommended movies including tconst
    """
    if not liked_movies_profile:
        logger.warning("Empty liked movies profile provided")
        return pd.DataFrame()
    
    # Find valid movies in the dataset
    valid_indices = []
    valid_movies = []
    
    for title_year in liked_movies_profile:
        try:
            label_idx = indices_map[title_year]
            position_idx = df.index.get_loc(label_idx)
            valid_indices.append(position_idx)
            valid_movies.append(title_year)
        except KeyError:
            logger.warning(f"Movie '{title_year}' not found in dataset, skipping")
            continue
    
    if not valid_indices:
        logger.error("No valid movies found in dataset from user's profile")
        return pd.DataFrame()
    
    logger.info(f"Using {len(valid_indices)} movies from user's profile for recommendations")
    
    # --- Aggregate Content Features ---
    # Average the feature vectors of all liked movies
    people_vectors = people_matrix[valid_indices]
    genre_vectors = genre_matrix[valid_indices]
    
    # Create aggregate profile by averaging, and ensure it's a standard numpy array
    avg_people_vector = np.asarray(np.mean(people_vectors, axis=0))
    avg_genre_vector = np.asarray(np.mean(genre_vectors, axis=0))
    
    # --- Content Score Calculation ---
    people_sim_scores = cosine_similarity(avg_people_vector, people_matrix)[0]
    genre_sim_scores = cosine_similarity(avg_genre_vector, genre_matrix)[0]
    
    w_people = 0.75 
    w_genre = 0.25
    combined_content_scores = (w_people * people_sim_scores) + (w_genre * genre_sim_scores)

    # Create similarity scores and exclude the movies the user already liked
    sim_scores = list(enumerate(combined_content_scores))
    
    # Filter out movies the user has already liked
    filtered_sim_scores = [(i, score) for i, score in sim_scores if i not in valid_indices]
    filtered_sim_scores = sorted(filtered_sim_scores, key=lambda x: x[1], reverse=True)[:500]
    
    # Extract indices and scores
    movie_indices = [i[0] for i in filtered_sim_scores]
    content_scores_list = [i[1] for i in filtered_sim_scores]

    # Build the recommendations DataFrame
    recs_df = df.iloc[movie_indices].copy()
    recs_df['content_score'] = content_scores_list
    
    # --- Additional Scoring Logic ---
    m = df['numVotes'].quantile(0.70)
    C = df['averageRating'].mean()
    
    def weighted_rating(x, m=m, C=C):
        v = x['numVotes']
        R = x['averageRating']
        return (v / (v + m) * R) + (m / (v + m) * C)
    
    recs_df['popularity_score'] = recs_df.apply(weighted_rating, axis=1)

    max_year = df['startYear'].max()
    min_year = df['startYear'].min()
    recs_df['recency_score'] = (recs_df['startYear'] - min_year) / (max_year - min_year)
    
    # Normalize scores
    if recs_df['content_score'].max() > 0:
        recs_df['content_score'] = recs_df['content_score'] / recs_df['content_score'].max()
    if recs_df['popularity_score'].max() > 0:
        recs_df['popularity_score'] = recs_df['popularity_score'] / recs_df['popularity_score'].max()
    
    # Calculate final scores
    w_content = 0.60
    w_popularity = 0.25
    w_recency = 0.15

    recs_df['final_score'] = (w_content * recs_df['content_score']) + \
                             (w_popularity * recs_df['popularity_score']) + \
                             (w_recency * recs_df['recency_score'])
    
    final_recs = recs_df.sort_values('final_score', ascending=False).head(20)
    
    # Return with tconst included for TMDb enrichment
    return final_recs[['tconst', 'primaryTitle', 'startYear', 'averageRating', 'genres']]