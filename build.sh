#!/bin/bash
# Build script for Render deployment

# Exit on error
set -e

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m flask db upgrade

# Apply Auth0 migrations
echo "Applying Auth0 migrations..."
python -m flask db migrate -m "Add Auth0 user ID field"
python -m flask db upgrade

# Create default avatar
python create_default_avatar.py

# Import roadmaps if needed
# python import_roadmaps.py

echo "Build completed successfully!"
