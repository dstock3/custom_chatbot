from model.database import get_db
from datetime import datetime

def insert_analysis(user_id, transcript_id, analysis):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO intel (user_id, transcript_id, analysis, analysis_date) VALUES (?, ?, ?, ?)",
                 (user_id, transcript_id, analysis, date_created))
    db.commit()

def get_analysis_by_user_id(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM intel WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def get_latest_analysis(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM intel WHERE user_id = ? ORDER BY analysis_date DESC LIMIT 1", (user_id,))
    return cursor.fetchone()

def update_analysis(id, analysis):
    db = get_db()
    db.execute("UPDATE intel SET analysis = ? WHERE id = ?", (analysis, id))
    db.commit()

def delete_analysis(id):
    db = get_db()
    db.execute("DELETE FROM intel WHERE id = ?", (id,))
    db.commit()
