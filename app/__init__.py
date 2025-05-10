from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import config
import json
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

# Flags to determine which services to use
USE_APPWRITE = os.environ.get('USE_APPWRITE', 'false').lower() == 'true'
USE_AUTH0 = os.environ.get('USE_AUTH0', 'false').lower() == 'true'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Initialize Auth0 if enabled
    if USE_AUTH0:
        from app.auth0 import auth0, setup_auth0
        setup_auth0(app)

    # Initialize Appwrite if enabled
    if USE_APPWRITE:
        from app.appwrite import appwrite
        appwrite.init_app(app)

        # Set up Appwrite collections
        with app.app_context():
            from app.appwrite.utils import setup_appwrite_collections
            setup_appwrite_collections()

    # Add custom Jinja2 filters
    app.jinja_env.filters['tojson'] = json.dumps
    app.jinja_env.filters['fromjson'] = lambda x: json.loads(x) if x else []

    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.roadmap import roadmap as roadmap_blueprint
    app.register_blueprint(roadmap_blueprint, url_prefix='/roadmap')

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app