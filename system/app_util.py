from assistant import main
from intel.meta_prompt import meta_prompt
from intel.keywords import extract_keywords
from intel.sentiment import get_sentiment
from intel.category import determine_category
from intel.remember import rememberance
from model.transcript import insert_transcript, update_transcript, get_subject, get_transcript_by_subject
from flask import request

def processPOST(req, user, subject=None):
    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = req.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript, display, auto_prompt, subject = processExchange(user, True, audio_file_path, subject)
            return chat_transcript, display, auto_prompt, subject

        # check if text input is provided
        text_input = req.form.get('text')
        if text_input:
            chat_transcript, display, auto_prompt, subject = processExchange(user, False, text_input, subject)
            return chat_transcript, display, auto_prompt, subject

def processExchange(user, isAudio, input, subject=None):
    if subject:
        fetchedTranscript = get_transcript_by_subject(subject)
        existing_messages = fetchedTranscript[2]
        chat_transcript, display = main(user, isAudio, input, existing_messages)
    else:
        chat_transcript, display = main(user, isAudio, input)
        
    if user['auto_prompt']:
        auto_prompt = meta_prompt(chat_transcript, user, 'auto_prompt')
    else:
        auto_prompt = None

    # If this is the first exchange, we need to establish the subject, sentiment, category, and keywords
    if len(chat_transcript) == 1:
        print(chat_transcript)
        new_exchange = chat_transcript[0]
        category = determine_category(chat_transcript)
        
        # If the user has opted in to data collection, we will collect sentiment and keywords
        if (user['collect_data']):
            sentiment = get_sentiment(new_exchange['user_message'])
            combined_text = new_exchange['user_message'] + ' ' + new_exchange['assistant_message']
            keywords = extract_keywords(combined_text)

            # call "rememberance" function in order to provide info from long term memory in present context
            memories = rememberance(keywords)
            
        else:
            sentiment = None
            keywords = []

        subject = meta_prompt(chat_transcript, user, 'subject')        
        messages = [
            {"role": "user", "content": new_exchange["user_message"]},
            {"role": "assistant", "content": new_exchange["assistant_message"]}
        ]
        insert_transcript(subject, messages, keywords, category, sentiment)
    else:
        if type(chat_transcript) == tuple:
            chat_transcript = reformat_messages(chat_transcript[2])
    
        latest_exchange = chat_transcript[-1]
        
        if not subject:
            previous_exchange = chat_transcript[-2]
            subject = get_subject(previous_exchange['user_message'])
        update_transcript(subject, latest_exchange)
        
    return chat_transcript, display, auto_prompt, subject

def reformat_messages(messages):
    formatted_messages = []
    for message in messages:
        if message['role'] == 'user':
            formatted_messages.append({'user_message': message['content'], 'assistant_message': ''})
        elif message['role'] == 'assistant':
            if formatted_messages:
                formatted_messages[-1]['assistant_message'] = message['content']
            else:
                formatted_messages.append({'user_message': '', 'assistant_message': message['content']})
    return formatted_messages
