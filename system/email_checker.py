import imaplib
import email
from bs4 import BeautifulSoup
import re
import textwrap
from system import config

imap_server = 'imap.gmail.com'
pw = config.PW
user = config.USER

def login(username, password):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def fetch_emails(mail, folder='inbox', read_only=True):
    mail.select(folder, read_only)
    _, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()
    
    emails = []
    for mail_id in mail_ids:
        _, msg_data = mail.fetch(mail_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        emails.append(msg)
    
    return emails

def clean_text(text):
    # Remove CSS between style tags
    clean_text = re.sub('<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Remove inline CSS inside style attributes
    clean_text = re.sub('style="[^"]*"', '', clean_text)
    # Remove any HTML tags
    clean_text = re.sub('<[^>]*>', '', clean_text)
    # Remove any HTML entities (e.g., '&nbsp;')
    clean_text = re.sub('&[^;]+;', '', clean_text)
    # Replace newline and carriage return characters with spaces
    clean_text = clean_text.replace('\r', '').replace('\n', '').replace('\t', '')
    # Replace consecutive whitespace characters with a single space
    clean_text = re.sub('\s+', ' ', clean_text).strip()
    # Wrap the text at a specific column width (e.g., 80 characters)
    clean_text = '\n'.join(textwrap.wrap(clean_text, width=80))
    return clean_text

def extract_email_info(msg):
    email_info = {
        'subject': msg['subject'],
        'from': msg['from'],
        'to': msg['to'],
        'date': msg['date'],
        'body': ''
    }

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True)
                soup = BeautifulSoup(html_content, 'html.parser')
                email_info['body'] = clean_text(soup.get_text())
                break
    else:
        email_info['body'] = clean_text(msg.get_payload(decode=True).decode())

    return email_info

def check_emails():
    mail = login(user, pw)
    emails = fetch_emails(mail)

    email_infos = []
    for msg in emails:
        email_info = extract_email_info(msg)
        email_infos.append(email_info)

    return email_infos

if __name__ == '__main__':
    email_infos = check_emails()
    for info in email_infos:
        print(info)