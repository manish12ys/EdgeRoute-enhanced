#!/usr/bin/env python
"""
Script to set up Appwrite for EdgeRoute application.
This script will:
1. Create the Appwrite database and collections
2. Import roadmaps from JSON files to Appwrite
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Appwrite is enabled
if os.environ.get('USE_APPWRITE', 'false').lower() != 'true':
    print("Appwrite is not enabled. Set USE_APPWRITE=true in .env file.")
    sys.exit(1)

# Check if Appwrite credentials are set
required_vars = [
    'APPWRITE_ENDPOINT',
    'APPWRITE_PROJECT_ID',
    'APPWRITE_API_KEY',
    'APPWRITE_DATABASE_ID'
]

missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    print(f"Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set these variables in your .env file.")
    sys.exit(1)

# Import Flask app and Appwrite utils
from app import create_app
from app.appwrite.utils import setup_appwrite_collections, import_roadmaps_to_appwrite

# Create Flask app
app = create_app()

# Set up Appwrite collections
with app.app_context():
    print("Setting up Appwrite collections...")
    if setup_appwrite_collections():
        print("Appwrite collections set up successfully.")
    else:
        print("Failed to set up Appwrite collections.")
        sys.exit(1)
    
    # Import roadmaps to Appwrite
    print("Importing roadmaps to Appwrite...")
    if import_roadmaps_to_appwrite():
        print("Roadmaps imported to Appwrite successfully.")
    else:
        print("Failed to import roadmaps to Appwrite.")
        sys.exit(1)

print("Appwrite setup completed successfully!")
