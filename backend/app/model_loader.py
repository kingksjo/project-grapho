import os
import joblib
import logging
from huggingface_hub import hf_hub_download

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model_assets():
    """
    Downloads and loads all necessary model assets from the Hugging Face Hub.
    """
    logger.info("=== Starting model assets loading process ===")
    
    # Your Hugging Face repository ID
    REPO_ID = "KSJO/grapho-recommendation-engine"
    
    # Get the Hugging Face token from environment variable
    hf_token = os.getenv('HUGGINGFACE_TOKEN')
    
    if not hf_token:
        logger.warning("HUGGINGFACE_TOKEN not found in environment variables. Proceeding without authentication.")
        logger.warning("This may cause issues if the repository is private or if you hit rate limits.")
    else:
        logger.info("Hugging Face token found in environment variables.")
    
    # The list of files to download
    files_to_download = [
        'movies_df.pkl',
        'people_tfidf_matrix.pkl',
        'genre_tfidf_matrix.pkl',
        'indices_map.pkl'
    ]
    
    logger.info(f"Repository: {REPO_ID}")
    logger.info(f"Files to download: {len(files_to_download)} files")
    
    loaded_assets = {}
    successful_downloads = 0
    failed_downloads = 0
    
    for i, filename in enumerate(files_to_download, 1):
        logger.info(f"[{i}/{len(files_to_download)}] Downloading {filename}...")
        
        try:
            # Download the file from the Hub with authentication
            file_path = hf_hub_download(
                repo_id=REPO_ID, 
                filename=filename,
                token=hf_token  # Add the token here
            )
            
            logger.info(f"✓ Successfully downloaded {filename} to {file_path}")
            
            # Load the downloaded file into memory
            asset_key = filename.replace('.pkl', '') # e.g., 'movies_df'
            loaded_assets[asset_key] = joblib.load(file_path)
            
            # Log the loaded asset info
            if hasattr(loaded_assets[asset_key], 'shape'):
                logger.info(f"✓ Loaded {filename} as '{asset_key}' with shape: {loaded_assets[asset_key].shape}")
            elif hasattr(loaded_assets[asset_key], '__len__'):
                logger.info(f"✓ Loaded {filename} as '{asset_key}' with {len(loaded_assets[asset_key])} items")
            else:
                logger.info(f"✓ Loaded {filename} as '{asset_key}'")
            
            successful_downloads += 1
            
        except Exception as e:
            logger.error(f"✗ Failed to download/load {filename}: {str(e)}")
            failed_downloads += 1
            # Continue with other files instead of failing completely
            continue
    
    # Summary feedback
    logger.info("=== Model assets loading summary ===")
    logger.info(f"Successful downloads: {successful_downloads}/{len(files_to_download)}")
    logger.info(f"Failed downloads: {failed_downloads}/{len(files_to_download)}")
    
    if failed_downloads > 0:
        logger.warning(f"⚠️  {failed_downloads} files failed to load. Some functionality may be limited.")
    
    if successful_downloads == len(files_to_download):
        logger.info("🎉 All model assets loaded successfully!")
    else:
        logger.warning("⚠️  Some model assets failed to load. Check the logs above for details.")
    
    logger.info(f"Loaded assets: {list(loaded_assets.keys())}")
    logger.info("=== Model assets loading process completed ===")
    
    return loaded_assets