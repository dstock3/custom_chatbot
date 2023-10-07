from model.database import get_db
import json

def get_insights(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT * 
        FROM insights 
        WHERE user_id=?
    """, (user_id,))

    data = cursor.fetchone()

    if data is None:
        return None
    
    insights = {
        "user_id": data[1],
        "basic": json.loads(data[2]),
        "health": json.loads(data[3]),
        "fam": json.loads(data[4]),
        "work": json.loads(data[5]),
        "big5": json.loads(data[6]),
        "ent": json.loads(data[7])
    }

    return insights

def save_insights(user_id, insights):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO insights (user_id, basic, health, fam, work, big5, ent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, json.dumps(insights['basic']), json.dumps(insights['health']), json.dumps(insights['fam']), json.dumps(insights['work']), json.dumps(insights['big5']), json.dumps(insights['ent'])))
    
    db.commit()






