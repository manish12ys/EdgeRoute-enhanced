import os
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.services.account import Account
from appwrite.services.storage import Storage
from appwrite.services.teams import Teams
from appwrite.services.functions import Functions
from appwrite.id import ID

class AppwriteConfig:
    """Configuration for Appwrite services"""
    
    def __init__(self, app=None):
        self.client = None
        self.databases = None
        self.users = None
        self.account = None
        self.storage = None
        self.teams = None
        self.functions = None
        
        # Appwrite configuration
        self.endpoint = os.environ.get('APPWRITE_ENDPOINT', 'https://cloud.appwrite.io/v1')
        self.project_id = os.environ.get('APPWRITE_PROJECT_ID')
        self.api_key = os.environ.get('APPWRITE_API_KEY')
        
        # Database configuration
        self.database_id = os.environ.get('APPWRITE_DATABASE_ID')
        
        # Collection IDs
        self.users_collection_id = os.environ.get('APPWRITE_USERS_COLLECTION_ID', 'users')
        self.roadmaps_collection_id = os.environ.get('APPWRITE_ROADMAPS_COLLECTION_ID', 'roadmaps')
        self.roadmap_nodes_collection_id = os.environ.get('APPWRITE_ROADMAP_NODES_COLLECTION_ID', 'roadmap_nodes')
        self.user_progress_collection_id = os.environ.get('APPWRITE_USER_PROGRESS_COLLECTION_ID', 'user_progress')
        self.comments_collection_id = os.environ.get('APPWRITE_COMMENTS_COLLECTION_ID', 'comments')
        self.custom_roadmaps_collection_id = os.environ.get('APPWRITE_CUSTOM_ROADMAPS_COLLECTION_ID', 'custom_roadmaps')
        self.custom_roadmap_nodes_collection_id = os.environ.get('APPWRITE_CUSTOM_ROADMAP_NODES_COLLECTION_ID', 'custom_roadmap_nodes')
        
        # Storage configuration
        self.storage_id = os.environ.get('APPWRITE_STORAGE_ID', 'profile_pictures')
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Appwrite with Flask app"""
        # Get configuration from app
        self.endpoint = app.config.get('APPWRITE_ENDPOINT', self.endpoint)
        self.project_id = app.config.get('APPWRITE_PROJECT_ID', self.project_id)
        self.api_key = app.config.get('APPWRITE_API_KEY', self.api_key)
        self.database_id = app.config.get('APPWRITE_DATABASE_ID', self.database_id)
        
        # Initialize Appwrite client
        self.client = Client()
        self.client.set_endpoint(self.endpoint)
        self.client.set_project(self.project_id)
        self.client.set_key(self.api_key)
        
        # Initialize services
        self.databases = Databases(self.client)
        self.users = Users(self.client)
        self.account = Account(self.client)
        self.storage = Storage(self.client)
        self.teams = Teams(self.client)
        self.functions = Functions(self.client)
        
        # Add to app context
        app.appwrite = self
        
        # Add to app config
        app.config['APPWRITE_CONFIG'] = self

# Create a singleton instance
appwrite = AppwriteConfig()

def get_appwrite():
    """Get the Appwrite instance"""
    return appwrite
