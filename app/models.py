import os
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import jwt
from . import bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db_session, Base

class User(Base):
    __tablename__ = 'users'
    #__table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    #username = Column(String, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, 4
        ).decode()
        #    password, os.getenv('BCRYPT_LOG_ROUNDS')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

 
    def __repr__(self):
        return f"<User(username='{self.username}')>"


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        with db_session() as s:
            # check whether auth token has been blacklisted
            res = s.query(BlacklistToken).filter_by(token=str(auth_token)).first()
            if res:
                return True
            else:
                return False



class Queue(Base):
    __tablename__ = 'queues'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String)
    cron = Column(String)
    user = relationship("User")
    #user = relationship("User", back_populates = "users")
    #user_id = Column(Integer, ForeignKey('users.id'))
    #user = relationship("User", back_populates="users")
    #post = relationship("Post", back_populates="postss")
    
    def __repr__(self):
        return f"<Queue(name='{self.name}', cron='{self.cron}')>"

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String)
    message = Column(String)
    queue_id = Column(Integer)
    #queue_id = Column(Integer, ForeignKey('users.id'))
    #queue = relationship("User", back_populates="users")

    def __repr__(self):
        return f"<Post(name='{self.title}', cron='{self.message}')>"


User.queues = relationship("Queue", order_by = Queue.id, back_populates = "user")
