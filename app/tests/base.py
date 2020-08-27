from flask_testing import TestCase

from app import app
from app.database import init_db, drop_db, Base, engine


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        #app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        #Base.metadata.drop_all(bind=engine)
        #Base.metadata.create_all(bind=engine)
        init_db()
        #return

    def tearDown(self):
        #drop_db()
        return

