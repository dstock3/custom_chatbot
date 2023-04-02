from flask import Flask, request, render_template, redirect, url_for
from assistant import main
from model.database import insert_transcript, get_all_transcripts, init_db, delete_all_transcripts
from model.user import get_user, update_user_preferences, init_user_table, delete_user
from intel.personalities import personalities

app = Flask(__name__)
init_db(app)
init_user_table(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    #delete_all_transcripts()
    #history = get_all_transcripts()
    history = []
    user = get_user()
    print(user)
    
    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = request.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript, display = main(True, input=audio_file_path)

            #for exchange in chat_transcript:
                #insert_transcript(exchange['user_message'], exchange['assistant_message'])
            #history = get_all_transcripts()
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)
 
        # check if text input is provided
        text_input = request.form.get('text')
        if text_input:
            chat_transcript, display = main(False, input=text_input)

            #for exchange in chat_transcript:
                #insert_transcript(exchange['user_message'], exchange['assistant_message'])
            #history = get_all_transcripts()
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)
    return render_template('index.html', history=history, user=user)

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    user = get_user()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            # Delete the user's data and redirect to the preferences page
            delete_user(user['user_id'])
            return redirect(url_for('preferences'))
        else:
            # Update the user's preferences
            voice_command = request.form.get('voice_command') == 'on'
            voice_response = request.form.get('voice_response') == 'on'
            update_user_preferences(
                user['user_id'],
                name=request.form.get('username'),
                voice_command=voice_command,
                voice_response=voice_response,
                personality=request.form.get('personality'),
            )
    elif not user['name'] or not user['voice_command'] or not user['voice_response'] or not user['personality']:
        # Redirect to the preferences page if the user has not set their preferences yet
        return redirect(url_for('preferences'))
    
    return render_template('preferences.html', user=user, personality_options=personalities)

if __name__ == '__main__':
    app.run(debug=True)

