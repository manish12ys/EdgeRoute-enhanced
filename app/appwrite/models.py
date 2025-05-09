import json
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from appwrite.id import ID
from appwrite.query import Query
from appwrite.exception import AppwriteException
from .config import get_appwrite

class AppwriteModel:
    """Base class for Appwrite models"""
    
    collection_id = None
    
    @classmethod
    def get_database(cls):
        """Get the Appwrite database service"""
        appwrite = get_appwrite()
        return appwrite.databases
    
    @classmethod
    def get_collection_id(cls):
        """Get the collection ID for this model"""
        return cls.collection_id
    
    @classmethod
    def get_database_id(cls):
        """Get the database ID"""
        appwrite = get_appwrite()
        return appwrite.database_id
    
    @classmethod
    def create(cls, data):
        """Create a new document in the collection"""
        database = cls.get_database()
        document_id = data.get('id', ID.unique())
        
        try:
            result = database.create_document(
                database_id=cls.get_database_id(),
                collection_id=cls.get_collection_id(),
                document_id=document_id,
                data=data
            )
            return cls(**result)
        except AppwriteException as e:
            print(f"Error creating document: {e}")
            return None
    
    @classmethod
    def get(cls, document_id):
        """Get a document by ID"""
        database = cls.get_database()
        
        try:
            result = database.get_document(
                database_id=cls.get_database_id(),
                collection_id=cls.get_collection_id(),
                document_id=document_id
            )
            return cls(**result)
        except AppwriteException as e:
            print(f"Error getting document: {e}")
            return None
    
    @classmethod
    def list(cls, queries=None, limit=25):
        """List documents in the collection"""
        database = cls.get_database()
        
        try:
            result = database.list_documents(
                database_id=cls.get_database_id(),
                collection_id=cls.get_collection_id(),
                queries=queries,
                limit=limit
            )
            
            documents = []
            for doc in result['documents']:
                documents.append(cls(**doc))
            
            return documents
        except AppwriteException as e:
            print(f"Error listing documents: {e}")
            return []
    
    @classmethod
    def update(cls, document_id, data):
        """Update a document"""
        database = cls.get_database()
        
        try:
            result = database.update_document(
                database_id=cls.get_database_id(),
                collection_id=cls.get_collection_id(),
                document_id=document_id,
                data=data
            )
            return cls(**result)
        except AppwriteException as e:
            print(f"Error updating document: {e}")
            return None
    
    @classmethod
    def delete(cls, document_id):
        """Delete a document"""
        database = cls.get_database()
        
        try:
            database.delete_document(
                database_id=cls.get_database_id(),
                collection_id=cls.get_collection_id(),
                document_id=document_id
            )
            return True
        except AppwriteException as e:
            print(f"Error deleting document: {e}")
            return False


class User(UserMixin, AppwriteModel):
    """User model for Appwrite"""
    
    collection_id = 'users'
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('$id')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password_hash = kwargs.get('password_hash')
        self.name = kwargs.get('name', '')
        self.bio = kwargs.get('bio', '')
        self.profile_pic = kwargs.get('profile_pic', 'default.jpg')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.is_admin = kwargs.get('is_admin', False)
    
    def set_password(self, password):
        """Set the password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the password is correct"""
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email"""
        users = cls.list(queries=[Query.equal('email', email)])
        return users[0] if users else None
    
    @classmethod
    def find_by_username(cls, username):
        """Find a user by username"""
        users = cls.list(queries=[Query.equal('username', username)])
        return users[0] if users else None


class Roadmap(AppwriteModel):
    """Roadmap model for Appwrite"""
    
    collection_id = 'roadmaps'
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('$id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.category = kwargs.get('category')
        self.difficulty = kwargs.get('difficulty')
        self.tags = kwargs.get('tags', '').split(',') if kwargs.get('tags') else []
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @classmethod
    def find_by_category(cls, category):
        """Find roadmaps by category"""
        return cls.list(queries=[Query.equal('category', category)])


class RoadmapNode(AppwriteModel):
    """RoadmapNode model for Appwrite"""
    
    collection_id = 'roadmap_nodes'
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('$id')
        self.roadmap_id = kwargs.get('roadmap_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.links = json.loads(kwargs.get('links', '[]'))
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @classmethod
    def find_by_roadmap(cls, roadmap_id):
        """Find nodes by roadmap ID"""
        return cls.list(queries=[Query.equal('roadmap_id', roadmap_id)])


class UserProgress(AppwriteModel):
    """UserProgress model for Appwrite"""
    
    collection_id = 'user_progress'
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('$id')
        self.user_id = kwargs.get('user_id')
        self.roadmap_id = kwargs.get('roadmap_id')
        self.node_id = kwargs.get('node_id')
        self.completed = kwargs.get('completed', False)
        self.completed_at = kwargs.get('completed_at')
    
    @classmethod
    def find_by_user_and_roadmap(cls, user_id, roadmap_id):
        """Find progress by user ID and roadmap ID"""
        return cls.list(queries=[
            Query.equal('user_id', user_id),
            Query.equal('roadmap_id', roadmap_id)
        ])
    
    @classmethod
    def find_by_user_roadmap_node(cls, user_id, roadmap_id, node_id):
        """Find progress by user ID, roadmap ID, and node ID"""
        progress = cls.list(queries=[
            Query.equal('user_id', user_id),
            Query.equal('roadmap_id', roadmap_id),
            Query.equal('node_id', node_id)
        ])
        return progress[0] if progress else None
