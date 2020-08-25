from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import db_session, Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String)
    #queue = relationship("Queue", back_populates="queues")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"

class Queue(Base):
    __tablename__ = 'queues'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cron = Column(String)
    user_id = Column(Integer)
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

    #query = db_session.query_property()
    
    def __repr__(self):
        return f"<Post(name='{self.title}', cron='{self.message}')>"

