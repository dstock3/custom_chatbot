from model.database import get_db

def create_user(name, system_name, voice_command, voice_response, model, personality, auto_prompt, theme_pref):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user (name, system_name, voice_command, voice_response, model, personality, auto_prompt, theme_pref)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, system_name, voice_command, voice_response, model, personality, auto_prompt, theme_pref))
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
            "personality": user[6],
            "auto_prompt": user[7],
            "theme_pref": user[8]
        }
    return None

def update_user_preferences(user_id, name, system_name, voice_command, voice_response, model, personality, auto_prompt, theme_pref):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE user
        SET name=?, system_name=?, voice_command=?, voice_response=?, model=?, personality=?, auto_prompt=?, theme_pref=?
        WHERE user_id=?
    """, (name, system_name, voice_command, voice_response, model, personality, auto_prompt, theme_pref, user_id))
    db.commit()

def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM user WHERE user_id=?", (user_id,))
    db.commit()
