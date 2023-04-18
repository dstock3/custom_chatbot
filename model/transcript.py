from model.database import get_db
from datetime import datetime
import json

def insert_transcript(subject, messages, keywords, category):
    db = get_db()
    date_created = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    messages_json = json.dumps(messages)  # Serialize the messages list
    keywords_json = json.dumps(keywords)
    db.execute("INSERT INTO transcripts (subject, messages, keywords, date_created, category) VALUES (?, ?, ?, ?, ?)",
                 (subject, messages_json, keywords_json, date_created, category))
    db.commit()

def update_transcript(subject, messages):
    db = get_db()
    messages_json = json.dumps(messages)

    db.execute("UPDATE transcripts SET messages = ? WHERE subject = ?", (messages_json, subject))
    db.commit()

def get_transcript_by_subject(subject):
    db = get_db()
    transcript = db.execute("SELECT * FROM transcripts WHERE subject = ?", (subject,)).fetchone()
    if transcript:
        return transcript[0], transcript[1], json.loads(transcript[2]), json.loads(transcript[3]), transcript[4], transcript[5]
    return None

def delete_transcript_by_subject(subject):
    db = get_db()
    db.execute("DELETE FROM transcripts WHERE subject = ?", (subject,))
    db.commit()

def delete_all_transcripts():
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) FROM transcripts")
    db.execute("DELETE FROM transcripts")
    db.commit()
    cursor = db.execute("SELECT COUNT(*) FROM transcripts")

def get_all_transcripts():
    db = get_db()
    transcripts = db.execute("SELECT * FROM transcripts").fetchall()
    return [(row[0], row[1], json.loads(row[2]), json.loads(row[3]), row[4], row[5]) for row in transcripts]

def search_conversations(keyword):
    db = get_db()
    keyword = f"%{keyword}%"
    cursor = db.execute("SELECT id, subject, messages, date_created, category FROM transcripts WHERE keywords LIKE ? ORDER BY id DESC", (keyword,))
    return [(row[0], row[1], json.loads(row[2]), row[3], row[4]) for row in cursor.fetchall()]

def get_subject(user_message):
    db = get_db()
    cursor = db.execute("SELECT subject FROM transcripts WHERE messages LIKE ? LIMIT 1", (f"%{user_message}%",))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
