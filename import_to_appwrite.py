import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set USE_APPWRITE to True
os.environ['USE_APPWRITE'] = 'true'

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import Flask app and models
from app import create_app
from app.appwrite.utils import setup_appwrite_collections, import_roadmaps_to_appwrite

def main():
    """Import data to Appwrite"""
    print("Starting import to Appwrite...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Set up Appwrite collections
        print("Setting up Appwrite collections...")
        if setup_appwrite_collections():
            print("Appwrite collections set up successfully")
        else:
            print("Failed to set up Appwrite collections")
            return
        
        # Import roadmaps
        print("Importing roadmaps to Appwrite...")
        if import_roadmaps_to_appwrite():
            print("Roadmaps imported successfully")
        else:
            print("Failed to import roadmaps")
            return
    
    print("Import to Appwrite completed successfully")

if __name__ == "__main__":
    main()
