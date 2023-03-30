from flask import Flask, request, render_template
from assistant import main
from model.database import insert_transcript, get_all_transcripts, init_db, delete_all_transcripts
from model.user import create_user, get_user, update_user_preferences
from intel import personalities

app = Flask(__name__)
#init_db(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    #delete_all_transcripts()
    #history = get_all_transcripts()
    history = []

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
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history)
 
        # check if text input is provided
        text_input = request.form.get('text')
        if text_input:
            chat_transcript, display = main(False, input=text_input)

            #for exchange in chat_transcript:
                #insert_transcript(exchange['user_message'], exchange['assistant_message'])
            #history = get_all_transcripts()
            return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history)
    return render_template('index.html', history=history)

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    user = get_user()

    if request.method == 'POST':
        user['username'] = request.form.get('username')
        user['voice_command'] = request.form.get('voice_command')
        user['voice_response'] = request.form.get('voice_response')
        user['personality'] = request.form.get('personality')

    return render_template('preferences.html', user=user, personality_options=personalities)

if __name__ == '__main__':
    app.run(debug=True)

