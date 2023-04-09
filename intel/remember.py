from intel.keywords import extract_keywords
from model.database import get_db
from intel.meta_prompt import meta_prompt
from model.user import get_user
import json

def search_conversations(keyword):
    db = get_db()
    keyword = f"%{keyword}%"
    cursor = db.execute("SELECT id, subject, user_message, assistant_message, date_created, keywords FROM transcripts WHERE keywords LIKE ? ORDER BY id DESC", (keyword,))
    return cursor.fetchall()

def remember_when(user_input):
    user = get_user()
    keywords = extract_keywords(user_input)
    if len(keywords) != 0:
        db = get_db()
        conversations = []
        for keyword in keywords:
            results = search_conversations(keyword)
            for result in results:
                conversation = {
                    "subject": result[1],
                    "user_message": result[2],
                    "assistant_message": result[3],
                    "date_created": result[4],
                    "keywords": json.loads(result[5]),
                    "relevance_score": 0,
                }
                if keyword in conversation["keywords"]:
                    conversation["relevance_score"] += conversation["keywords"].index(keyword)
                conversations.append(conversation)
        if len(conversations) > 0:
            # get the conversation with the highest relevance score
            conversations = sorted(conversations, key=lambda x: x["relevance_score"], reverse=True)
            conversation = conversations[0]
            response = meta_prompt(conversation, user, "recall")
            print(response)
            
            return response
    return None