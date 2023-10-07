from assistant import main
from intel.meta_prompt import meta_prompt
from intel.keywords import extract_keywords
from intel.sentiment import get_sentiment
from intel.category import determine_category
from intel.remember import rememberance
from model.transcript import insert_transcript, update_transcript, get_subject, get_transcript_by_subject
from insights.integrate_insights import respond_based_on_category
from flask import request, Request
from system.format import reformat_messages
from typing import List, Dict, Tuple, Optional, Any
from debug.types import TranscriptDict
from debug.debug_wrapper import debug

def processPOST(
    req: Request,
    user: Dict[str, Any],
    subject: Optional[str] = None,
    user_info: Optional[List[str]] = None
) -> Tuple[List[Dict[str, str]], Any, Any, str]:
    """    
    Used within the index and subject routes to handle POST requests. It takes in a Flask Request object, a dictionary of user settings, and an optional subject. It processes uploaded audio files and text inputs to generate a chat transcript, display settings, auto prompt settings, and a subject for redirection.
    """

    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = req.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript, display, auto_prompt, subject = processExchange(user, True, audio_file_path, subject, user_info=user_info)
            return chat_transcript, display, auto_prompt, subject or ""

        # check if text input is provided
        text_input = req.form.get('text')
        if text_input:
            chat_transcript, display, auto_prompt, subject = processExchange(user, False, text_input, subject, user_info=user_info)
            return chat_transcript, display, auto_prompt, subject or ""
    #default return
    return [], None, None, ""

def processExchange(
    user: Dict[str, Any], 
    isAudio: bool, 
    input: str, 
    subject: Optional[str] = None,
    user_info: Optional[List[str]] = None
) -> Tuple[List[TranscriptDict], Optional[Any], Any, Optional[str]]:
    """
    Process an exchange between a user and the assistant based on the user's settings. Used within processPOST. Takes in a dictionary of user settings, a boolean indicating whether the input is an audio file or text, a string containing the input, and an optional subject. It returns a chat transcript, display settings, auto prompt settings, and a subject for redirection.
    """
    if subject:
        fetchedTranscript = get_transcript_by_subject(subject)
        existing_messages = fetchedTranscript[2]
        chat_transcript, display = main(user, isAudio, input, existing_messages, user_info)
    else:
        chat_transcript, display = main(user, isAudio, input, user_info=user_info)
        
    if user['auto_prompt']:
        auto_prompt = meta_prompt(chat_transcript, user, 'auto_prompt')
    else:
        auto_prompt = None

    # If this is the first exchange, we need to establish the subject, sentiment, category, and keywords
    if len(chat_transcript) == 1:
        new_exchange = chat_transcript[0]
        category = determine_category(chat_transcript)
        
        # If the user has opted in to data collection, we will collect sentiment and keywords
        if (user['collect_data']):
            sentiment = get_sentiment(new_exchange['user_message'])
            combined_text = new_exchange['user_message'] + ' ' + new_exchange['assistant_message']
            keywords = extract_keywords(combined_text)

            # Call "rememberance" function in order to provide info from long term memory in present context
            # memories = rememberance(keywords, chat_transcript)
            # print("Response from rememberance:")
            # print(memories)
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
