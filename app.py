from flask import Flask, request, render_template
from assistant import main
from model.database import init_db
from model.transcript import insert_transcript, get_all_transcripts, delete_all_transcripts, update_transcript, get_subject
from model.user import get_user, create_user, update_user_preferences, init_user_table, delete_user
from intel.personalities import personalities
from intel.meta_prompt import meta_prompt
from intel.keywords import extract_keywords
from intel.sentiment import get_sentiment

app = Flask(__name__)
init_db(app)
init_user_table(app)

def processExchange(user, isAudio, audio_file_path):
    chat_transcript, display = main(user, isAudio, audio_file_path)

    # If this is the first exchange, we need to create the subject, sentiment, and keywords
    if len(chat_transcript) == 1:
        new_exchange = chat_transcript[0]
        sentiment = get_sentiment(new_exchange['user_message'])
        combined_text = new_exchange['user_message'] + ' ' + new_exchange['assistant_message']
        keywords = extract_keywords(combined_text)
        subject = meta_prompt(chat_transcript, user, 'subject')
        messages = [
            {"role": "user", "content": new_exchange["user_message"]},
            {"role": "assistant", "content": new_exchange["assistant_message"]}
        ]
        insert_transcript(subject, messages, keywords)
    else:
        latest_exchange = chat_transcript[-1]
        previous_exchange = chat_transcript[-2]
        subject = get_subject(previous_exchange['user_message'])
        update_transcript(subject, latest_exchange)

    print(chat_transcript)
    return chat_transcript, display

@app.route('/', methods=['GET', 'POST'])
def index():
    #delete_all_transcripts()
    history = get_all_transcripts()
    
    user = get_user()
    
    if not user:
        create_user('User', 'Assistant', False, False, 'gpt-3.5-turbo', 'default')
        user = get_user()

    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = request.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript, display = processExchange(user, True, audio_file_path)
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)
 
        # check if text input is provided
        text_input = request.form.get('text')
        if text_input:
            chat_transcript, display = processExchange(user, False, text_input)
            history = get_all_transcripts()
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)
    return render_template('index.html', history=history, user=user)

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    history = []
    user = get_user()
    
    model_options = {
        'davinci',
        'curie',
        'babbage',
        'ada',
        'gpt-3.5-turbo'
    }

    if request.method == 'POST':
        if 'delete' in request.form:
            # Delete the user's data and redirect to the preferences page
            delete_user(user['user_id'])
            return render_template('index.html', history=history, user=user)
        else:
            # Update the user's preferences
            voice_command = request.form.get('voice_command') == 'on'
            voice_response = request.form.get('voice_response') == 'on'
            update_user_preferences(
                user['user_id'],
                name=request.form.get('username'),
                system_name=request.form.get('system_name'),
                voice_command=voice_command,
                voice_response=voice_response,
                model=request.form.get('model'),
                personality=request.form.get('personality')
            )
            user = get_user(user['user_id'])  # Update user information after updating preferences
    
    return render_template('preferences.html', user=user, personality_options=personalities, model_options=model_options)

@app.route('/history', methods=['GET'])
def history():
    user = get_user()
    history = get_all_transcripts()
    return render_template('history.html', user=user, history=history)

if __name__ == '__main__':
    app.run(debug=True)
