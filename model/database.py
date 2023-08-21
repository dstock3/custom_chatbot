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
            theme_pref TEXT NOT NULL,
            collect_data BOOLEAN NOT NULL);''')
        
        # Create search_history table
        db.execute('''
            CREATE TABLE IF NOT EXISTS search_history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            search_text TEXT NOT NULL,
            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(user_id));''')

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
            basic TEXT,
            health TEXT,
            fam TEXT,
            work TEXT,
            big5 TEXT,
            FOREIGN KEY(user_id) REFERENCES user(user_id));
            ''')
        
        # Create intel table if it does not exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS intel
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transcript_id INTEGER,
            analysis TEXT NOT NULL,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(transcript_id) REFERENCES transcripts(id));
            ''')
        
        # Create persona table if it does not exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS persona
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(user_id));
            ''')
        
        db.commit()