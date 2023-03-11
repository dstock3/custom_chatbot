import sqlite3
from flask import g

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
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS transcripts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_message TEXT NOT NULL,
                     assistant_message TEXT NOT NULL);''')
        db.commit()

def insert_transcript(user_message, assistant_message):
    db = get_db()
    db.execute("INSERT INTO transcripts (user_message, assistant_message) VALUES (?, ?)",
                 (user_message, assistant_message))
    db.commit()

def get_all_transcripts():
    db = get_db()
    cursor = db.execute("SELECT id, user_message, assistant_message FROM transcripts")
    return cursor.fetchall()
