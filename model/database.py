import sqlite3
from flask import g
import os
from datetime import datetime

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
        db.execute("DROP TABLE IF EXISTS transcripts")
        db.execute('''CREATE TABLE transcripts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_message TEXT NOT NULL,
                     assistant_message TEXT NOT NULL,
                     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
        db.commit()

    if not os.path.exists(DATABASE):
        with open(DATABASE, 'w'):
            pass

def insert_transcript(user_message, assistant_message):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO transcripts (user_message, assistant_message, date_created) VALUES (?, ?, ?)",
                 (user_message, assistant_message, date_created))
    db.commit()

def delete_all_transcripts():
    db = get_db()
    db.execute("DELETE FROM transcripts")
    db.commit()

def get_all_transcripts():
    db = get_db()
    cursor = db.execute("SELECT id, user_message, assistant_message, date_created FROM transcripts ORDER BY id DESC")
    return cursor.fetchall()

def get_user():
    # Replace the following with the actual query to get the user from the database
    user = {
        'username': 'JohnDoe',
        'voice_command': 'On',
        'personality': 'quirky',  # You can replace 'quirky' with the default personality
        'voice_response': True
    }
    return user


