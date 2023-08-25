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

def get_notes(user_id):
  db = get_db()
  notes = db.execute(
    'SELECT * FROM notes WHERE user_id = ?', (user_id,)  
  ).fetchall()

  return notes

def delete_note(note_id):
  db = get_db()
  db.execute('DELETE FROM notes WHERE id = ?', (note_id,))
  db.commit()

def get_note(note_id):
  db = get_db()
  note = db.execute(
    'SELECT * FROM notes WHERE id = ?', (note_id,)   
  ).fetchone()

  return note

