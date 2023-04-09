import sqlite3
from flask import g
import os
from datetime import datetime
import json

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

def insert_transcript(subject, user_message, assistant_message, keywords):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    keywords_json = json.dumps(keywords)
    db.execute("INSERT INTO transcripts (subject, user_message, assistant_message, keywords, date_created) VALUES (?, ?, ?, ?, ?)",
                 (subject, user_message, assistant_message, keywords_json, date_created))
    db.commit()

def delete_all_transcripts():
    db = get_db()
    db.execute("DELETE FROM transcripts")
    db.commit()

def get_all_transcripts():
    db = get_db()
    transcripts = db.execute("SELECT * FROM transcripts").fetchall()
    return [(row[0], row[1], row[2], row[3], json.loads(row[4]), row[5]) for row in transcripts]

def search_conversations(keyword):
    db = get_db()
    keyword = f"%{keyword}%"
    cursor = db.execute("SELECT id, subject, user_message, assistant_message, date_created FROM transcripts WHERE keywords LIKE ? ORDER BY id DESC", (keyword,))
    return cursor.fetchall()