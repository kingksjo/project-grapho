# Global assets storage
# This module holds the loaded model assets that can be accessed by any part of the application

# A dictionary to hold our loaded model assets
model_assets = {}

def get_model_assets():
    """Get the current model assets dictionary"""
    return model_assets

def update_model_assets(new_assets):
    """Update the model assets dictionary"""
    model_assets.update(new_assets)

def clear_model_assets():
    """Clear all model assets"""
    model_assets.clear()
