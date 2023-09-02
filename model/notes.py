from model.database import get_db
from datetime import datetime
import json

def create_note(user_id, note, keywords):
    db = get_db()
    cursor = db.cursor()
    keywords_json = json.dumps(keywords)
    cursor.execute("""
        INSERT INTO notes (user_id, note, keywords)
        VALUES (?, ?, ?)
    """, (user_id, note, keywords_json))
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

