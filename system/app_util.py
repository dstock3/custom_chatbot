from assistant import main
from intel.meta_prompt import meta_prompt
from intel.keywords import extract_keywords
from intel.sentiment import get_sentiment
from intel.category import determine_category
from model.transcript import insert_transcript, update_transcript, get_subject, get_transcript_by_subject
from flask import request, render_template

def processPOST(req, user):
    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = req.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript, display = processExchange(user, True, audio_file_path)
            return chat_transcript, display

        # check if text input is provided
        text_input = req.form.get('text')
        if text_input:
            chat_transcript, display = processExchange(user, False, text_input)
            print("chat_transcript:")
            print(chat_transcript)
            return chat_transcript, display
            
def processExchange(user, isAudio, audio_file_path, subject=None):
    if subject:
        chat_transcript = get_transcript_by_subject(subject)
        display = None
        print("Transcript in processExchange:", chat_transcript) 
    else:
        chat_transcript, display = main(user, isAudio, audio_file_path)

    print(chat_transcript)

    # If this is the first exchange, we need to establish the subject, sentiment, category, and keywords
    if len(chat_transcript) == 1:
        new_exchange = chat_transcript[0]
        category = determine_category(chat_transcript)
        sentiment = get_sentiment(new_exchange['user_message'])
        combined_text = new_exchange['user_message'] + ' ' + new_exchange['assistant_message']
        keywords = extract_keywords(combined_text)
        subject = meta_prompt(chat_transcript, user, 'subject')
        messages = [
            {"role": "user", "content": new_exchange["user_message"]},
            {"role": "assistant", "content": new_exchange["assistant_message"]}
        ]
        insert_transcript(subject, messages, keywords, category)
    else:
        latest_exchange = chat_transcript[-1]
        previous_exchange = chat_transcript[-2]
        if not subject:
            subject = get_subject(previous_exchange['user_message'])
        update_transcript(subject, latest_exchange)

    return chat_transcript, display

def reformat_messages(messages):
    formatted_messages = []
    for i in range(0, len(messages), 2):
        user_message = messages[i]['content'] if messages[i]['role'] == 'user' else ''
        assistant_message = messages[i + 1]['content'] if messages[i + 1]['role'] == 'assistant' else ''
        formatted_messages.append({'user_message': user_message, 'assistant_message': assistant_message})
    print("Reformatted messages:", formatted_messages) 
    return formatted_messages