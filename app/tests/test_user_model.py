import unittest

from app.database import db_session
from app.models import User
from app.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        with db_session() as s:
            s.add(user)
            s.commit()
        auth_token = user.encode_auth_token(user.id)
        #self.assertTrue(isinstance(auth_token, bytes))

if __name__ == '__main__':
    unittest.main()

