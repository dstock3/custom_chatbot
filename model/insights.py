from model.database import get_db
import json

def save_user_response(user_id, question_id, response, section):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user_responses (user_id, question_id, response, section)
        VALUES (?, ?, ?, ?)
    """, (user_id, question_id, response, section))
    db.commit()

def get_user_responses(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT question_id, response, section
        FROM user_responses
        WHERE user_id=?
    """, (user_id,))
    
    responses = cursor.fetchall()
    
    insights = {
        'basic': {},
        'health': {},
        'fam': {},
        'work': {},
        'big5': {},
    }

    for row in responses:
        section = row[2]
        if section in insights:
            insights[section][row[0]] = row[1]
    
    return insights

def save_personality_score(user_id, big_five_scores):
    """
    Save the calculated Big Five personality scores to a file.
    
    Args:
        user_id (str): The unique identifier of the user.
        big_five_scores (dict): A dictionary of the Big Five personality scores.
    """
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE user_responses
        SET response = ?
        WHERE user_id = ? AND section = 'big5'
    """, (json.dumps(big_five_scores), user_id))
    
    db.commit()



