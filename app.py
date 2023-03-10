from flask import Flask, request, render_template
from assistant import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      audio_file = request.files['audio']
      if audio_file:
          audio_file_path = "audio_file.wav"
          audio_file.save(audio_file_path)
          chat_transcript = main(audio_file_path)
          return chat_transcript
      else:
          return 'No audio file received'
    else:
        return render_template('index.html')
      
if __name__ == '__main__':
    app.run(debug=True)

