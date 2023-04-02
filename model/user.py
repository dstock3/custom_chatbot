from model.database import get_db

def init_user_table(app):
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     voice_command BOOLEAN NOT NULL,
                     voice_response BOOLEAN NOT NULL,
                     personality TEXT NOT NULL);''')
        db.commit()

def create_user(name, voice_command=True, voice_response=True, personality="quirky"):
    db = get_db()
    db.execute("INSERT INTO users (name, voice_command, voice_response, personality) VALUES (?, ?, ?, ?)",
                 (name, voice_command, voice_response, personality))
    db.commit()

def get_user(user_id=None):
    db = get_db()
    if user_id:
        cursor = db.execute("SELECT user_id, name, voice_command, voice_response, personality FROM users WHERE user_id = ?", (user_id,))
    else:
        cursor = db.execute("SELECT user_id, name, voice_command, voice_response, personality FROM users LIMIT 1")

    row = cursor.fetchone()
    if row:
        return {
            'user_id': row[0],
            'name': row[1],
            'voice_command': row[2],
            'voice_response': row[3],
            'personality': row[4]
        }
    else:
        if user_id:
            return None
        else:
            create_user(name="New User")
            return get_user()
        
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.commit()

def update_user_preferences(user_id, name=None, voice_command=None, voice_response=None, personality=None):
    db = get_db()
    db.execute("UPDATE users SET name = ?, voice_command = ?, voice_response = ?, personality = ? WHERE user_id = ?", (name, voice_command, voice_response, personality, user_id))
    db.commit()