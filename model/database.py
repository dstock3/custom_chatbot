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
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    with app.app_context():
        db = get_db()
        
        # Create transcripts table if it does not exist
        db.execute('''CREATE TABLE IF NOT EXISTS transcripts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_message TEXT NOT NULL,
                     assistant_message TEXT NOT NULL,
                     keywords TEXT,
                     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
        
        # Create users table if it does not exist
        db.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     preference_1 TEXT,
                     preference_2 TEXT);''')

        db.commit()

def insert_transcript(user_message, assistant_message, keywords):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO transcripts (user_message, assistant_message, keywords, date_created) VALUES (?, ?, ?, ?)",
                 (user_message, assistant_message, keywords, date_created))  # Remove the ",".join(keywords)
    db.commit()

def delete_all_transcripts():
    db = get_db()
    db.execute("DELETE FROM transcripts")
    db.commit()

def get_all_transcripts():
    db = get_db()
    cursor = db.execute("SELECT id, user_message, assistant_message, keywords, date_created FROM transcripts ORDER BY id DESC")
    return cursor.fetchall()


def search_conversations(keyword):
    db = get_db()
    keyword = f"%{keyword}%"
    cursor = db.execute("SELECT id, user_message, assistant_message, date_created FROM transcripts WHERE keywords LIKE ? ORDER BY id DESC", (keyword,))
    return cursor.fetchall()