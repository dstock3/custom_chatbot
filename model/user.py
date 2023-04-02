import sqlite3
from model.database import get_db

def init_user_table(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                assistant_name TEXT NOT NULL,
                voice_command BOOLEAN NOT NULL,
                voice_response BOOLEAN NOT NULL,
                personality TEXT NOT NULL
            )
        """)
        db.commit()

def create_user(name, assistant_name, voice_command, voice_response, personality):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user (name, assistant_name, voice_command, voice_response, personality)
        VALUES (?, ?, ?, ?, ?)
    """, (name, assistant_name, voice_command, voice_response, personality))
    db.commit()

def get_user(user_id=None):
    db = get_db()
    cursor = db.cursor()

    if user_id is None:
        cursor.execute("SELECT * FROM user LIMIT 1")
    else:
        cursor.execute("SELECT * FROM user WHERE user_id=?", (user_id,))
    
    user = cursor.fetchone()

    if user:
        return {
            "user_id": user[0],
            "name": user[1],
            "assistant_name": user[2],
            "voice_command": user[3],
            "voice_response": user[4],
            "personality": user[5]
        }
    return None

def update_user_preferences(user_id, name, assistant_name, voice_command, voice_response, personality):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE user
        SET name=?, assistant_name=?, voice_command=?, voice_response=?, personality=?
        WHERE user_id=?
    """, (name, assistant_name, voice_command, voice_response, personality, user_id))
    db.commit()


def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM user WHERE user_id=?", (user_id,))
    db.commit()
