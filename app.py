from flask import Flask, request, render_template
from assistant import main
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        # check if audio file is uploaded
        audio_file = request.files.get('audio')
        if audio_file:
            audio_file_path = "audio_file.wav"
            audio_file.save(audio_file_path)
            chat_transcript = main(audio_file=audio_file_path)

            return render_template('index.html', chat_transcript=chat_transcript)
            
        # check if text input is provided
        text_input = request.form.get('text')
        if text_input:
            chat_transcript = main(text_input=text_input)
            print(chat_transcript)
            return render_template('index.html', chat_transcript=chat_transcript)
        else:
            return 'No audio file or text input received'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
