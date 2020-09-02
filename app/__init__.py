import os

from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session

from app.database import db_session

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


#def create_app(test_config=None):
# App init
app = Flask(__name__, instance_relative_config=True)

# App config
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/.*": {"origins": "http://localhost"}})
app.session = scoped_session(db_session, scopefunc=_app_ctx_stack.__ident_func__)

# Init plugins
bcrypt = Bcrypt(app)

# Database
from app.database import *
init_app(app)

# JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Load endpoints
from . import users
app.register_blueprint(users.bp)
from . import posts
app.register_blueprint(posts.bp)
from . import queues
app.register_blueprint(queues.bp)
from . import auth
app.register_blueprint(auth.bp)

#return app
