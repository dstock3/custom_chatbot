from model.database import get_db

def add_search_history(user_id, search_text):
    db = get_db()
    db.execute('INSERT INTO search_history (user_id, search_text) VALUES (?, ?)', (user_id, search_text))
    db.commit()

def get_search_history(user_id):
    #need to enable user to view search history in user preferences
    db = get_db()
    cur = db.execute('SELECT search_text, search_date FROM search_history WHERE user_id = ? ORDER BY search_date DESC', (user_id,))
    return cur.fetchall()

def delete_search_history(user_id):
    db = get_db()
    db.execute('DELETE FROM search_history WHERE user_id = ?', (user_id,))
    db.commit()
