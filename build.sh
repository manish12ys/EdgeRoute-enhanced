#!/bin/bash
# Build script for Render deployment

# Exit on error
set -e

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m flask db upgrade

# Create default avatar
python create_default_avatar.py

# Import roadmaps if needed
# python import_roadmaps.py

# Set up Appwrite collections if USE_APPWRITE is true
if [ "$USE_APPWRITE" = "true" ]; then
  echo "Setting up Appwrite collections..."
  python -c "from app import create_app; from app.appwrite.utils import setup_appwrite_collections; app = create_app(); with app.app_context(): setup_appwrite_collections()"

  # Import roadmaps to Appwrite
  echo "Importing roadmaps to Appwrite..."
  python -c "from app import create_app; from app.appwrite.utils import import_roadmaps_to_appwrite; app = create_app(); with app.app_context(): import_roadmaps_to_appwrite()"
fi

echo "Build completed successfully!"
