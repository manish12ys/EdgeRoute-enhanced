from flask import redirect, url_for, session, request, current_app, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.auth import auth
from app.auth0.auth import get_login_url, get_logout_url, get_user_info
import json
from urllib.parse import urlencode
import os

@auth.route("/auth0/login")
def auth0_login():
    """Route for Auth0 login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Check if Auth0 is enabled
    if not current_app.config.get('USE_AUTH0', False):
        flash('Auth0 login is not enabled', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get the Auth0 login URL
    return get_login_url()

@auth.route("/callback")
def callback():
    """Auth0 callback route"""
    # Get the Auth0 client
    auth0 = current_app.auth0
    
    # Get the access token
    token = auth0.authorize_access_token()
    
    # Get the user info
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    
    # Store user info in session
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo.get('name', ''),
        'picture': userinfo.get('picture', ''),
        'email': userinfo.get('email', '')
    }
    
    # Check if user exists in database
    user = User.query.filter_by(email=userinfo['email']).first()
    
    if not user:
        # Create new user
        user = User(
            username=userinfo.get('nickname', userinfo['email'].split('@')[0]),
            email=userinfo['email'],
            avatar='default.jpg'
        )
        
        # Generate a random password (user will never use it since Auth0 handles auth)
        import secrets
        random_password = secrets.token_hex(16)
        user.password = random_password
        
        # Set Auth0 user ID
        user.auth0_user_id = userinfo['sub']
        
        # Add user to database
        db.session.add(user)
        db.session.commit()
    else:
        # Update Auth0 user ID if not set
        if not user.auth0_user_id:
            user.auth0_user_id = userinfo['sub']
            db.session.commit()
    
    # Log in the user
    login_user(user)
    
    # Redirect to the next page or home
    next_page = session.get('next', url_for('main.index'))
    return redirect(next_page)

@auth.route("/auth0/logout")
def auth0_logout():
    """Route for Auth0 logout"""
    # Clear session
    session.clear()
    
    # Log out the user
    logout_user()
    
    # Get the Auth0 logout URL
    return redirect(get_logout_url())
