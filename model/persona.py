from model.database import get_db

def create_persona(user_id, persona_name, persona_description, temperature):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO persona (user_id, persona_name, persona_description, temperature)
        VALUES (?, ?, ?, ?)
    """, (user_id, persona_name, persona_description, temperature))
    
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

def delete_all_personas():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM persona
    """)

    db.commit()
