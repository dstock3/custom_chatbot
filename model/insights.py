from model.database import get_db
import sqlite3

def create_insights_table():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(user_id)
        )
    """)
    db.commit()

def save_response(user_id, question, response):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO insights (user_id, question, response)
        VALUES (?, ?, ?)
    """, (user_id, question, response))
    db.commit()
    
def get_insights():
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT question, response FROM insights")
        insights = cursor.fetchall()

        if insights:
            return [{"question": insight[0], "response": insight[1]} for insight in insights]
    except sqlite3.OperationalError:
        create_insights_table()

    return None

