from intel.keywords import extract_keywords
from model.database import get_db
from intel.meta_prompt import meta_prompt
from model.user import get_user
import json

def search_conversations(keyword):
    db = get_db()
    user = get_user()
    
    ai_name = user["system_name"]
    user_name = user["name"]

    # Disregard the user's name and the AI's name
    if keyword == ai_name or keyword == user_name:
        return None

    keyword = f"%{keyword}%"
    cursor = db.execute("""
        SELECT id, subject, messages, date_created
        FROM transcripts
        WHERE id IN (
            SELECT transcripts.id
            FROM transcripts, json_each(transcripts.messages)
            WHERE json_each.value LIKE ?
        )
        ORDER BY id DESC
    """, (keyword,))
    results = [(row[0], row[1], json.loads(row[2]), row[3]) for row in cursor.fetchall()]

    return results

def determine_relevance(user_input):
    keywords = extract_keywords(user_input)
    if len(keywords) != 0:
        conversations = []
        for keyword in keywords:
            results = search_conversations(keyword)

            for result in results:
                messages = result[2]
                user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
                assistant_messages = [msg["content"] for msg in messages if msg["role"] == "assistant"]

                conversation = {
                    "subject": result[1],
                    "user_message": user_messages,
                    "assistant_message": assistant_messages,
                    "date_created": result[3],
                    "relevance_score": 0,
                }

                for kw in keywords:
                    if kw in user_messages or kw in assistant_messages:
                        conversation["relevance_score"] += 1

                conversations.append(conversation)
        return conversations


#need to create two functions: one to handle recall at onset of conversation and one to handle recall after transcript has been created. One will be called in index and the other will be called in subject

def recall_at_onset(user_input):
    conversations = determine_relevance(user_input)
    return conversations

def recall_based_on_transcript(transcript):
    subject = transcript[1]
    user_input = transcript[2][0]['content']
    conversations = determine_relevance(user_input)

    for conversation in conversations:
        if conversation['subject'] == subject:
            conversations.remove(conversation)

    return conversations

def remember_when(user_input):
    user = get_user()
    conversations = determine_relevance(user_input)

    if len(conversations) > 0:
        # get the conversation with the highest relevance score
        conversations = sorted(conversations, key=lambda x: x["relevance_score"], reverse=True)
        conversation = conversations[0]

        response = meta_prompt(conversation, user, "recall")
        return response
    return None

