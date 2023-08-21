from model.database import get_db

def create_persona(user_id, persona_name, persona_description):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO persona (user_id, persona_name, persona_description)
        VALUES (?, ?, ?)
    """, (user_id, persona_name, persona_description))
    
    db.commit()

def get_persona_by_user_id(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM persona WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def delete_persona(persona_name):
    db = get_db()
    db.execute("DELETE FROM persona WHERE persona_name = ?", (persona_name,))
    db.commit()
