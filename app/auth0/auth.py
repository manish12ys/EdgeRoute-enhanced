import json
import os
from urllib.parse import urlencode
from functools import wraps

from authlib.integrations.flask_client import OAuth
from flask import current_app, redirect, session, url_for, request
from flask_login import current_user

# Auth0 configuration
oauth = OAuth()
auth0 = None

def setup_auth0(app):
    """Initialize Auth0 with Flask app"""
    global auth0
    
    # Get configuration from app
    auth0_client_id = app.config.get('AUTH0_CLIENT_ID')
    auth0_client_secret = app.config.get('AUTH0_CLIENT_SECRET')
    auth0_domain = app.config.get('AUTH0_DOMAIN')
    auth0_audience = app.config.get('AUTH0_AUDIENCE')
    
    # Initialize OAuth
    oauth.init_app(app)
    
    # Register Auth0 client
    auth0 = oauth.register(
        'auth0',
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        api_base_url=f'https://{auth0_domain}',
        access_token_url=f'https://{auth0_domain}/oauth/token',
        authorize_url=f'https://{auth0_domain}/authorize',
        client_kwargs={
            'scope': 'openid profile email',
            'audience': auth0_audience
        },
    )
    
    # Add to app context
    app.auth0 = auth0
    
    # Add to app config
    app.config['AUTH0_CONFIG'] = {
        'client_id': auth0_client_id,
        'client_secret': auth0_client_secret,
        'domain': auth0_domain,
        'audience': auth0_audience
    }
    
    return auth0

def requires_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            # Build the login URL and redirect
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def get_token_auth_header():
    """Get the Access Token from the Authorization Header"""
    auth = request.headers.get('Authorization', None)
    if not auth:
        return None
    
    parts = auth.split()
    
    if parts[0].lower() != 'bearer':
        return None
    
    if len(parts) == 1:
        return None
    
    if len(parts) > 2:
        return None
    
    token = parts[1]
    return token

def get_user_info(access_token):
    """Get user info from Auth0"""
    global auth0
    
    if not auth0:
        auth0 = oauth.create_client('auth0')
    
    resp = auth0.get('userinfo', token=access_token)
    return resp.json()

def get_login_url():
    """Get the Auth0 login URL"""
    global auth0
    
    if not auth0:
        auth0 = oauth.create_client('auth0')
    
    callback_url = url_for('auth.callback', _external=True)
    return auth0.authorize_redirect(redirect_uri=callback_url)

def get_logout_url():
    """Get the Auth0 logout URL"""
    domain = current_app.config.get('AUTH0_DOMAIN')
    client_id = current_app.config.get('AUTH0_CLIENT_ID')
    return_to = url_for('main.index', _external=True)
    
    params = {
        'returnTo': return_to,
        'client_id': client_id
    }
    
    return f'https://{domain}/v2/logout?{urlencode(params)}'
