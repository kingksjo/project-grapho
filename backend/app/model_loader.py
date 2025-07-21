# backend/app/model_loader.py
import os
import joblib
from huggingface_hub import hf_hub_download

def load_model_assets():
    """
    Downloads and loads all necessary model assets from the Hugging Face Hub.
    """
    print("--- Loading model assets from Hugging Face Hub ---")
    
    # Your Hugging Face repository ID
    REPO_ID = "KSJO/grapho-recommendation-engine"
    
    # The list of files to download
    files_to_download = [
        'movies_df.pkl',
        'people_tfidf_matrix.pkl',
        'genre_tfidf_matrix.pkl',
        'indices_map.pkl'
    ]
    
    loaded_assets = {}
    
    for filename in files_to_download:
        print(f"Downloading {filename}...")
        # Download the file from the Hub, it will be cached locally
        file_path = hf_hub_download(repo_id=REPO_ID, filename=filename)
        
        # Load the downloaded file into memory
        asset_key = filename.replace('.pkl', '') # e.g., 'movies_df'
        loaded_assets[asset_key] = joblib.load(file_path)
        print(f"Loaded {filename} as '{asset_key}'")
        
    print("--- All model assets loaded successfully ---")
    return loaded_assets