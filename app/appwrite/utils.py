import os
import json
from appwrite.id import ID
from appwrite.query import Query
from appwrite.exception import AppwriteException
from .config import get_appwrite
from .models import Roadmap, RoadmapNode, User, UserProgress

def setup_appwrite_collections():
    """Set up the Appwrite collections if they don't exist"""
    appwrite = get_appwrite()
    database_id = appwrite.database_id
    
    try:
        # Check if database exists, create if not
        try:
            appwrite.databases.get(database_id)
        except AppwriteException:
            appwrite.databases.create(database_id, 'EdgeRoute Database')
        
        # Create Users collection
        try:
            appwrite.databases.get_collection(database_id, 'users')
        except AppwriteException:
            collection = appwrite.databases.create_collection(
                database_id=database_id,
                collection_id='users',
                name='Users'
            )
            
            # Add attributes
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='username',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='email',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='password_hash',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='name',
                size=255,
                required=False
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='bio',
                size=1000,
                required=False
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='users',
                key='profile_pic',
                size=255,
                required=False,
                default='default.jpg'
            )
            
            appwrite.databases.create_boolean_attribute(
                database_id=database_id,
                collection_id='users',
                key='is_admin',
                required=False,
                default=False
            )
            
            # Create indexes
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='users',
                key='email_index',
                type='key',
                attributes=['email']
            )
            
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='users',
                key='username_index',
                type='key',
                attributes=['username']
            )
        
        # Create Roadmaps collection
        try:
            appwrite.databases.get_collection(database_id, 'roadmaps')
        except AppwriteException:
            collection = appwrite.databases.create_collection(
                database_id=database_id,
                collection_id='roadmaps',
                name='Roadmaps'
            )
            
            # Add attributes
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmaps',
                key='title',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmaps',
                key='description',
                size=5000,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmaps',
                key='category',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmaps',
                key='difficulty',
                size=50,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmaps',
                key='tags',
                size=500,
                required=False
            )
            
            # Create indexes
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='roadmaps',
                key='category_index',
                type='key',
                attributes=['category']
            )
        
        # Create RoadmapNodes collection
        try:
            appwrite.databases.get_collection(database_id, 'roadmap_nodes')
        except AppwriteException:
            collection = appwrite.databases.create_collection(
                database_id=database_id,
                collection_id='roadmap_nodes',
                name='Roadmap Nodes'
            )
            
            # Add attributes
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmap_nodes',
                key='roadmap_id',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmap_nodes',
                key='title',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmap_nodes',
                key='description',
                size=10000,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='roadmap_nodes',
                key='links',
                size=5000,
                required=False,
                default='[]'
            )
            
            # Create indexes
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='roadmap_nodes',
                key='roadmap_id_index',
                type='key',
                attributes=['roadmap_id']
            )
        
        # Create UserProgress collection
        try:
            appwrite.databases.get_collection(database_id, 'user_progress')
        except AppwriteException:
            collection = appwrite.databases.create_collection(
                database_id=database_id,
                collection_id='user_progress',
                name='User Progress'
            )
            
            # Add attributes
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='user_progress',
                key='user_id',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='user_progress',
                key='roadmap_id',
                size=255,
                required=True
            )
            
            appwrite.databases.create_string_attribute(
                database_id=database_id,
                collection_id='user_progress',
                key='node_id',
                size=255,
                required=True
            )
            
            appwrite.databases.create_boolean_attribute(
                database_id=database_id,
                collection_id='user_progress',
                key='completed',
                required=True,
                default=False
            )
            
            appwrite.databases.create_datetime_attribute(
                database_id=database_id,
                collection_id='user_progress',
                key='completed_at',
                required=False
            )
            
            # Create indexes
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='user_progress',
                key='user_roadmap_index',
                type='key',
                attributes=['user_id', 'roadmap_id']
            )
            
            appwrite.databases.create_index(
                database_id=database_id,
                collection_id='user_progress',
                key='user_roadmap_node_index',
                type='key',
                attributes=['user_id', 'roadmap_id', 'node_id']
            )
        
        print("Appwrite collections setup complete")
        return True
    except AppwriteException as e:
        print(f"Error setting up Appwrite collections: {e}")
        return False

def import_roadmaps_to_appwrite():
    """Import roadmaps from JSON files to Appwrite"""
    # Get the roadmap data directory
    roadmap_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'roadmap_data')
    
    # Load roadmaps.json
    with open(os.path.join(roadmap_data_dir, 'roadmaps.json'), 'r', encoding='utf-8') as f:
        roadmaps_data = json.load(f)
    
    # Import each roadmap
    for roadmap_info in roadmaps_data['roadmaps']:
        roadmap_id = roadmap_info['id']
        
        # Check if roadmap already exists
        existing_roadmap = Roadmap.get(roadmap_id)
        if existing_roadmap:
            print(f"Roadmap {roadmap_id} already exists, skipping...")
            continue
        
        # Create roadmap
        tags_str = ','.join(roadmap_info['tags']) if 'tags' in roadmap_info else ''
        roadmap_data = {
            'id': roadmap_id,
            'title': roadmap_info['title'],
            'description': roadmap_info['description'],
            'category': roadmap_info['category'],
            'difficulty': roadmap_info['difficulty'],
            'tags': tags_str
        }
        
        roadmap = Roadmap.create(roadmap_data)
        if not roadmap:
            print(f"Failed to create roadmap {roadmap_id}")
            continue
        
        print(f"Created roadmap: {roadmap_id}")
        
        # Load roadmap nodes
        try:
            with open(os.path.join(roadmap_data_dir, f"{roadmap_id}.json"), 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            
            # Import each node
            for node_id, node_data in nodes_data.items():
                # Create node
                node_data = {
                    'id': node_id,
                    'roadmap_id': roadmap_id,
                    'title': node_data['title'],
                    'description': node_data['description'],
                    'links': json.dumps(node_data.get('links', []))
                }
                
                node = RoadmapNode.create(node_data)
                if not node:
                    print(f"Failed to create node {node_id} for roadmap {roadmap_id}")
                    continue
            
            print(f"Imported {len(nodes_data)} nodes for roadmap {roadmap_id}")
        except FileNotFoundError:
            print(f"No nodes file found for roadmap {roadmap_id}")
    
    print("Roadmap import complete")
    return True
