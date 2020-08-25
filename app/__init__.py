import os

from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from app.database import db_session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
#        SQLALCHEMY_DATABASE_URI='postgres+psycopg2://tweeter:tweeter@localhost:5432/tweeter',
#        SQLALCHEMY_NATIVE_UNICODE=True,
#        SQLALCHEMY_TRACK_MODIFICATIONS =False

    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"/.*": {"origins": "http://localhost"}})
    app.session = scoped_session(db_session, scopefunc=_app_ctx_stack.__ident_func__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #from . import database
    #database.init_app(app)
    db = SQLAlchemy(app)
    db.create_all()

    from . import users
    app.register_blueprint(users.bp)
    from . import posts
    app.register_blueprint(posts.bp)
    from . import queues
    app.register_blueprint(queues.bp)

    return app
