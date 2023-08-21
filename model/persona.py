from model.database import get_db

def create_persona(user_id, persona_name, persona_description):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO persona (user_id, persona_name, persona_description)
        VALUES (?, ?, ?)
    """, (user_id, persona_name, persona_description))
    
    db.commit()

def get_all_personas():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM persona
    """)

    return cursor.fetchall()

def get_persona(persona_name):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM persona WHERE persona_name = ?
    """, (persona_name,))

    return cursor.fetchall()

def delete_persona(persona_name):
    db = get_db()
    db.execute("DELETE FROM persona WHERE persona_name = ?", (persona_name,))
    db.commit()
