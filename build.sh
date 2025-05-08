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

echo "Build completed successfully!"
