from tinydb import TinyDB

import click
from flask import current_app, g
from flask.cli import with_appcontext


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
    db = get_db()
    db.table('queues')
    db.table('posts')

    # with current_app.open_resource('../db/schema.json') as f:
    #     db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

