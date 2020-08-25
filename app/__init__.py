import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tweeter.json'),
    )

    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"/.*": {"origins": "http://localhost"}})

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

    from . import users
    app.register_blueprint(users.bp)
    from . import posts
    app.register_blueprint(posts.bp)
    from . import queues
    app.register_blueprint(queues.bp)
    from . import schedulers
    app.register_blueprint(schedulers.bp)

    return app
