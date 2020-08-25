import time

from contextlib import contextmanager

import click
from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy


#db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://tweeter:tweeter@localhost:5432/tweeter'
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    convert_unicode=True
)

Base = declarative_base()
#Base.query = db_session.query_property()

@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = scoped_session(sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    ))
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        session.remove()

def get_db():
    if 'db' not in g:
        g.db = TinyDB(
            current_app.config['DATABASE']
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def test_db():
    try:
      test = get_db()
      test.close_db()
      return True
    except:
      return False


def init_db():
    print("init_db")
    #Base.metadata.drop_all(bind=engine)
    #Base.metadata.create_all(bind=engine)

def init_app(app):
    print("init_app")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

