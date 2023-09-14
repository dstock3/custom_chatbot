import re
from datetime import datetime

def markdown_to_html(message_content):
    plain_url_pattern = r'(?<!href=")(?P<url>https?://[^\s\)]+)'
    plain_url_replacement = r'<a href="\g<url>" target="_blank" rel="noopener noreferrer">\g<url></a>'
    message_content = re.sub(plain_url_pattern, plain_url_replacement, message_content)

    markdown_pattern = r'\[(?P<text>.*?)\]\((?P<url>https?://[^\)]+)\)'
    markdown_replacement = r'<a href="\g<url>" target="_blank" rel="noopener noreferrer">\g<text></a>'
    
    return re.sub(markdown_pattern, markdown_replacement, message_content)

def response_to_html_list(response_content):
    pattern = r'(\d+\.\s.*?<a href="https?://.*?".*?>.*?</a>.*?)(?:\n|$)'
    list_items = re.findall(pattern, response_content, re.DOTALL)
    
    if not list_items:
        return response_content

    html_list_items = ['<li class="assistant-list-item">{}</li>'.format(item) for item in list_items]
    ol = '<ol class="assistant-ordered-list">{}</ol>'.format(''.join(html_list_items))
    
    first_position = response_content.find("1.")
    intro = response_content[:first_position]
    outro = re.sub(pattern, '', response_content[first_position:], count=len(list_items))
    response_content = intro + ol + outro

    return response_content

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_incomplete_sentence(insight: str) -> str:
    # Remove any trailing sentence that doesn't end with a full stop (period).
    return re.sub(r'[^.]+\Z', '', insight).strip()

def format_date(date_string):
    #format date from 2020-04-01 12:00:00 to April 01, 2020
    date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%B %d, %Y")

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

def get_display(emoji_check, cleaned_text):
    display = emoji_check[0]
    processed_text = markdown_to_html(cleaned_text)
    final_text = response_to_html_list(processed_text)
    system_message = {"content": final_text, "role": "assistant"}
    return system_message, display