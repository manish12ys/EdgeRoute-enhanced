from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.auth import routes
from app.auth import auth0_routes
