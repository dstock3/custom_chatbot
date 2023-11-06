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

            #this method for determining relevance is not working. need to troubleshoot.
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

def get_relevant_conversation(conversations):
    if conversations is None:
        return []
    if len(conversations) > 0:
        # get the conversation with the highest relevance score
        conversations = sorted(conversations, key=lambda x: x["relevance_score"], reverse=True)
        conversation = conversations[0]
        return conversation

def recall_at_onset(user_input):
    conversations = determine_relevance(user_input)
    conversation = get_relevant_conversation(conversations)
    return conversation

def recall_based_on_transcript(transcript):
    subject = transcript[1]
    user_input = transcript[2][0]['content']
    conversations = determine_relevance(user_input)

    if conversations is None:
        return None
    else:
        for conversation in conversations:
            if conversation['subject'] == subject:
                conversations.remove(conversation)

    conversation = get_relevant_conversation(conversations)
    return conversation

def remember_when(user_input):
    user = get_user()
    conversations = determine_relevance(user_input)
    conversation = get_relevant_conversation(conversations)
    
    if response:
        response = meta_prompt(conversation, user, "recall")
        return response
    else:
        return None

