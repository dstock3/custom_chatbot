from model.database import get_db

def create_user(name, voice_command=None, voice_response=None, personality=None):
    db = get_db()
    db.execute("INSERT INTO users (name, voice_command, voice_response, personality) VALUES (?, ?, ?, ?)",
                 (name, voice_command, voice_response, personality))
    db.commit()

def get_user(user_id):
    db = get_db()
    cursor = db.execute("SELECT user_id, name, voice_command, voice_response, personality FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return {
            'user_id': row[0],
            'name': row[1],
            'voice_command': row[2],
            'voice_response': row[3],
            'personality': row[4]
        }
    return None

def update_user_preferences(user_id, name=None, voice_command=None, voice_response=None, personality=None):
    db = get_db()
    db.execute("UPDATE users SET name = ?, voice_command = ?, voice_response = ?, personality = ? WHERE user_id = ?", (name, voice_command, voice_response, personality, user_id))
    db.commit()