from model.database import get_db
from datetime import datetime

def create_note(note_content):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO notes (note_content)
        VALUES (?)
    """, (note_content,))
    db.commit()

def get_note():
    db = get_db()
    cursor = db.execute("SELECT * FROM notes ORDER BY date_created DESC LIMIT 1")
    return cursor.fetchone()
