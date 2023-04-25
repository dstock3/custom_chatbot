from flask import Flask, request, render_template, redirect, url_for
from collections import defaultdict
from model.database import init_db
from model.transcript import get_all_transcripts, get_transcript_by_subject, delete_transcript_by_subject, delete_all_transcripts, delete_keyword
from model.user import get_user, create_user, update_user_preferences, delete_user
from model.insights import create_insights_table, save_response, get_insights
from intel.personalities import personalities
from intel.model_options import model_options
from insights.questions import questions
from insights.process_results import process_results
from system.app_util import reformat_messages, processPOST
import json
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
init_db(app)

@app.context_processor
def inject_json():
    return dict(json=json)

@app.route('/clear_chat')
def clear_chat():
    global chat_transcript
    chat_transcript = []
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    history = get_all_transcripts()
    
    user = get_user()
    
    if not user:
        create_user('User', 'Assistant', False, False, 'gpt-3.5-turbo', 'default')
        user = get_user()
    if request.method == 'POST':
        chat_transcript, display = processPOST(request, user)
        return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)
    return render_template('index.html', history=history, user=user)

@app.route('/subject', methods=['GET', 'POST'])
def subject():
    user = get_user()
    subject = request.args.get('subject')
    transcript = get_transcript_by_subject(subject)
    history = get_all_transcripts()

    if request.method == 'POST':
        chat_transcript, display = processPOST(request, user, subject=subject)
        return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user)

    chat_transcript = reformat_messages(transcript[2])
    return render_template('index.html', chat_transcript=chat_transcript, history=history, user=user)

@app.route('/delete_transcript', methods=['POST'])
def delete_transcript():
    subject = request.form['subject']
    referrer = request.referrer
    parsed_referrer = urlparse(referrer)
    query_params = parse_qs(parsed_referrer.query)
    current_subject = query_params.get('subject', [None])[0]

    delete_transcript_by_subject(subject)

    if current_subject == subject:
        return redirect(url_for('index'))
    else:
        return redirect(request.referrer)

@app.route('/preferences', methods=['GET', 'POST', 'DELETE'])
def preferences():
    history = []
    user = get_user()
    
    if request.method == 'POST':
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
        user = get_user(user['user_id'])
        
    elif request.method == 'DELETE':
        delete_user(user['user_id'])
        delete_all_transcripts()
        return render_template('index.html', history=history, user=user)

    return render_template('preferences.html', user=user, personality_options=personalities, model_options=model_options)

@app.route('/history', methods=['GET'])
def history():
    user = get_user()
    history = get_all_transcripts()
    return render_template('history.html', user=user, history=history)

@app.route('/insights', methods=['GET'])
def insights():
    user = get_user()
    insights = get_insights()

    if not insights:
        create_insights_table()
        return redirect(url_for('questionnaire'))

    history = get_all_transcripts()
    return render_template('insights.html', user=user, history=history, insights=insights)

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    user = get_user()

    if request.method == 'POST':
        responses = defaultdict(dict)
        for question_id, response in request.form.items():
            section, question_number = question_id.split('-', 1)
            question_number = ''.join(question_number)

            question_text = None
            for question in questions[section]:
                if question['id'] == question_id:
                    question_text = question['text']
                    break

            save_response(user['user_id'], question_text, response)
            responses[section][question_text] = response

        insights = process_results(responses)

        for insight in insights:
            save_response(user['user_id'], insight['question'], insight['response'])

        return redirect(url_for('insights'))
    return render_template('questionnaire.html', user=user, questions=questions)

@app.route('/delete_keyword', methods=['POST'])
def delete_keyword():
    subject = request.form['subject']
    keyword = request.form['keyword']
    success = delete_keyword(subject, keyword)
    if success:
        print('Keyword successfully deleted', 'success')
    else:
        print('Error: Keyword not found or deletion failed', 'danger')
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)
