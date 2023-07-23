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
            sentiment TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')

        # Create user table if it does not exist        
        db.execute('''CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            system_name TEXT NOT NULL,
            voice_command BOOLEAN NOT NULL,
            voice_response BOOLEAN NOT NULL,
            model TEXT NOT NULL,
            personality TEXT NOT NULL,
            auto_prompt BOOLEAN NOT NULL,
            theme_pref TEXT NOT NULL);''')

        # Create user_responses table if it does not exist        
        db.execute('''CREATE TABLE IF NOT EXISTS user_responses (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(user_id)
            );''')

        # Create insights table if it does not exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS insights
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            section TEXT NOT NULL,
            summary TEXT,
            data TEXT,
            FOREIGN KEY(user_id) REFERENCES user(user_id));
            ''')

        db.commit()