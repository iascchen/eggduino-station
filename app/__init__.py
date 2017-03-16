# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_wtf.csrf import CSRFProtect
import sqlite3
import time

app = Flask(__name__)

app.config.from_object('config')

CSRFProtect(app)

###################
# DB Init
###################

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
        # db.row_factory = make_dicts
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    # print "query = " + query

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()


init_db()

###################
# View and models
###################

current_milli_time = lambda: int(round(time.time() * 1000))

from app import views, models, forms
