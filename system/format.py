import re

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
    html_list_items = ['<li class="assistant-list-item">{}</li>'.format(item) for item in list_items]
    ol = '<ol class="assistant-ordered-list">{}</ol>'.format(''.join(html_list_items))
    response_content = re.sub(pattern * len(list_items), ol, response_content, 1)
    
    return response_content

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)