import sqlite3
from flask import g
import os

DATABASE = 'data/chat.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    with app.app_context():
        db = get_db()
        
        # Create transcripts table if it does not exist
        db.execute('''CREATE TABLE IF NOT EXISTS transcripts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     subject TEXT NOT NULL,
                     messages TEXT NOT NULL,
                     keywords TEXT,
                     category TEXT,
                     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
        
        # Create user table if it does not exist
        db.execute('''CREATE TABLE IF NOT EXISTS user
                     (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     preference_1 TEXT,
                     preference_2 TEXT);''')

        db.commit()

