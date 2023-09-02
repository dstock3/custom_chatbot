from flask import Flask, request, render_template, redirect, url_for, flash
from collections import defaultdict
from model.database import init_db
from model.transcript import get_all_transcripts, get_transcript_by_subject, delete_transcript_by_subject, delete_all_transcripts, delete_keyword
from model.user import get_user, create_user, update_user_preferences, delete_user
from model.insights import save_insights, get_insights
from model.intel import get_analysis_by_user_id
from model.search_history import get_search_history, delete_search_history
from model.persona import create_persona, delete_all_personas
from intel.analysis import analysis
from intel.personalities import get_persona_list
from intel.model_options import model_options
from insights.questions import questions, category_descriptors 
from insights.process_results import process_results
from system.app_util import reformat_messages, processPOST
from system.theme_options import theme_options
from system.format import format_date
import json
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.jinja_env.filters['format_date'] = format_date
init_db(app)

@app.context_processor
def inject_json():
    return dict(json=json)

@app.route('/', methods=['GET', 'POST'])
def index():
    history = get_all_transcripts()
    user = get_user()
    
    if not user:
        create_user('User', 'Assistant', False, False, 'gpt-4', 'default', False, "light", False)
        user = get_user()
    if request.method == 'POST':
        chat_transcript, display, auto_prompt, subject = processPOST(request, user)

        return redirect(url_for('subject', subject=subject))
    return render_template('index.html', history=history, user=user)

def remove_consecutive_duplicates(chat_transcript):
    if not chat_transcript:
        return []

    cleaned_transcript = [chat_transcript[0]]

    for i in range(1, len(chat_transcript)):
        if chat_transcript[i] != chat_transcript[i-1]:
            cleaned_transcript.append(chat_transcript[i])

    return cleaned_transcript

@app.route('/subject', methods=['GET', 'POST'])
def subject():
    user = get_user()
    subject = request.args.get('subject')
    transcript = get_transcript_by_subject(subject)
    history = get_all_transcripts()

    if request.method == 'POST':
        if (user['collect_data']):
            insights = get_insights(user['user_id'])
            #need to figure out when analysis should be performed
            #analysis(insights, user, transcript)
        chat_transcript, display, auto_prompt, subject = processPOST(request, user, subject=subject)
        
        #need to figure out why the duplication is happening but this is a temporary fix
        chat_transcript = remove_consecutive_duplicates(chat_transcript)
        
        return render_template('index.html', chat_transcript=chat_transcript, display=display, history=history, user=user, auto_prompt=auto_prompt)

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
    search_history = get_search_history(user['user_id'])

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
            personality=request.form.get('personality'),
            auto_prompt=request.form.get('auto_prompt') == 'on',
            theme_pref=request.form.get('theme_pref'),
            collect_data=request.form.get('collect_data') == 'on'
        )
        flash('Your preferences have been saved!', 'success')
        user = get_user(user['user_id'])
        
    elif request.method == 'DELETE':
        delete_user(user['user_id'])
        delete_all_transcripts()
        delete_search_history(user['user_id'])
        delete_all_personas()
        return render_template('index.html', history=history, user=user)
    
    personas = get_persona_list()
    
    return render_template('preferences.html', user=user, personality_options=personas, model_options=model_options, theme_options=theme_options, search_history=search_history)

@app.route('/new_persona', methods=['POST'])
def new_persona():
    data = request.json
    user_id = data['user_id']
    persona_name = data['persona_name']
    persona_description = data['persona_description']
    temperature = data['temperature']

    create_persona(user_id, persona_name, persona_description, temperature)
    flash('Your preferences have been saved!', 'success')

    return redirect(request.referrer)

@app.route('/history', methods=['GET'])
def history():
    user = get_user()
    history = get_all_transcripts()
    search_history = get_search_history(user['user_id'])
    return render_template('history.html', user=user, history=history, search_history=search_history)

@app.route('/insights', methods=['GET'])
def insights():
    user = get_user()
    insights = get_insights(user['user_id'])

    if insights is None:
        return redirect(url_for('questionnaire'))

    return render_template('insights.html', user=user, insights=insights)

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    user = get_user()
    if user['collect_data'] == False:
        return redirect(url_for('message', message="You have opted out of data collection. If you'd like to see user insights, please go to the preferences page and opt in."))
    loading = False
    if request.method == 'POST':
        loading = True
        responses = defaultdict(dict)
        for question_id, response in request.form.items():
            question_text = None
            for section in questions:
                for question in questions[section]:
                    if question['id'] == question_id:
                        question_text = question['text']
                        break

            responses[question_id][question_text] = response

        insights, loading = process_results(responses)
        save_insights(user['user_id'], insights)
        return redirect(url_for('insights'))

    return render_template('questionnaire.html', user=user, questions=questions, category_desc =category_descriptors, loading=loading)

@app.route('/message', methods=['GET'])
def message():
    user = get_user()
    message = request.args.get('message')
    return render_template('message.html', user=user, message=message)

@app.route('/delete_keyword', methods=['POST'])
def del_keyword():
    subject = request.form['subject']
    keyword = request.form['keyword']
    success = delete_keyword(subject, keyword)

    return redirect(request.referrer)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    history = get_all_transcripts()
    user = get_user()
    try:
        delete_all_transcripts()
        flash('Your chat history has been erased', 'success')
        return render_template('index.html', history=history, user=user)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
