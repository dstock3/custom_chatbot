from model.database import get_db

def init_user_table(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                system_name TEXT NOT NULL,
                voice_command BOOLEAN NOT NULL,
                voice_response BOOLEAN NOT NULL,
                model TEXT NOT NULL,
                personality TEXT NOT NULL
            )
        """)
        db.commit()

def create_user(name, system_name, voice_command, voice_response, model, personality):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user (name, system_name, voice_command, voice_response, model, personality)
        VALUES (?, ?, ?, ?, ?)
    """, (name, system_name, voice_command, voice_response, model, personality))
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
            "system_name": user[2],
            "voice_command": user[3],
            "voice_response": user[4],
            "model": user[5],
            "personality": user[6]
        }
    return None

def update_user_preferences(user_id, name, system_name, voice_command, voice_response, model, personality):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE user
        SET name=?, system_name=?, voice_command=?, voice_response=?, model=?, personality=?
        WHERE user_id=?
    """, (name, system_name, voice_command, voice_response, model, personality, user_id))
    db.commit()

def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM user WHERE user_id=?", (user_id,))
    db.commit()
