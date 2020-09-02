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


class Queue(Base):
    __tablename__ = 'queues'
    #__table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String)
    cron = Column(String)
    user = relationship("User")
    
    def __repr__(self):
        return f"<Queue(name='{self.name}', cron='{self.cron}')>"


class Post(Base):
    __tablename__ = 'posts'
    #__table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    queue_id = Column(Integer, ForeignKey('queues.id'), nullable=False)
    title = Column(String)
    message = Column(String)
    queue = relationship("Queue")

    def __repr__(self):
        return f"<Post(name='{self.title}', cron='{self.message}')>"


User.queues = relationship("Queue", order_by = Queue.id, back_populates = "user")
Queue.posts = relationship("Post", order_by = Post.id, back_populates = "queue")
