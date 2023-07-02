from model.database import get_db
import json

def save_user_response(user_id, question_id, response):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO user_responses (user_id, question_id, response)
        VALUES (?, ?, ?)
    """, (user_id, question_id, response))
    db.commit()

def get_user_responses(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT question_id, response
        FROM user_responses
        WHERE user_id=?
    """, (user_id,))
    
    responses = cursor.fetchall()

    return [{"question_id": row[0], "response": row[1]} for row in responses]

def save_personality_score(user_id, big_five_scores):
    """
    Save the calculated Big Five personality scores to a file.
    
    Args:
        user_id (str): The unique identifier of the user.
        big_five_scores (dict): A dictionary of the Big Five personality scores.
    """
    # Create a dictionary to store user data
    user_data = {
        'user_id': user_id,
        'big_five_scores': big_five_scores
    }
    
    # Serialize the data to a JSON formatted string
    data = json.dumps(user_data)
    
    # Write the data to a file
    file_name = f"user_{user_id}_personality_scores.json"
    with open(file_name, 'w') as file:
        file.write(data)


