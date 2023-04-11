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
                     messages TEXT NOT NULL,
                     keywords TEXT,
                     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
        
        # Create users table if it does not exist
        db.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     preference_1 TEXT,
                     preference_2 TEXT);''')

        db.commit()

def insert_transcript(subject, messages, keywords):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    messages_json = json.dumps(messages)  # Serialize the messages list
    keywords_json = json.dumps(keywords)
    db.execute("INSERT INTO transcripts (subject, messages, keywords, date_created) VALUES (?, ?, ?, ?)",
                 (subject, messages_json, keywords_json, date_created))
    db.commit()

def update_transcript(subject, messages):
    db = get_db()
    messages_json = json.dumps(messages)

    db.execute("UPDATE transcripts SET messages = ?, keywords = ? WHERE subject = ?", (messages_json, subject))
    db.commit()

def get_transcript_by_subject(subject):
    db = get_db()
    transcript = db.execute("SELECT * FROM transcripts WHERE subject = ?", (subject,)).fetchone()
    if transcript:
        return transcript[0], transcript[1], json.loads(transcript[2]), json.loads(transcript[3]), transcript[4]
    return None

def delete_all_transcripts():
    db = get_db()
    db.execute("DELETE FROM transcripts")
    db.commit()

def get_all_transcripts():
    db = get_db()
    transcripts = db.execute("SELECT * FROM transcripts").fetchall()
    return [(row[0], row[1], json.loads(row[2]), json.loads(row[3]), row[4]) for row in transcripts]

def search_conversations(keyword):
    db = get_db()
    keyword = f"%{keyword}%"
    cursor = db.execute("SELECT id, subject, messages, date_created FROM transcripts WHERE keywords LIKE ? ORDER BY id DESC", (keyword,))
    return [(row[0], row[1], json.loads(row[2]), row[3]) for row in cursor.fetchall()]