import imaplib
import datetime
import email

imap_server = "imap.example.com"
imap_port = 993
username = "your_username"
password = "your_password"

# Connect to the IMAP server using imaplib.IMAP4_SSL and log in with your email credentials:
imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)
imap_connection.login(username, password)

# Select the mailbox you want to check, such as the inbox:
mailbox = "INBOX"
imap_connection.select(mailbox)

#Use imap_connection.search() to search for emails in the mailbox. For example, to search for all emails since a certain date:
since_date = datetime.date(2022, 1, 1)
since_date_str = since_date.strftime("%d-%b-%Y")

search_criteria = f"SINCE {since_date_str}"
status, email_ids = imap_connection.search(None, search_criteria)

email_id = email_ids[0]
status, email_data = imap_connection.fetch(email_id, "(RFC822)")

email_message = email.message_from_bytes(email_data[0][1])
subject = email_message["Subject"]
body = email_message.get_payload()

#After you have finished retrieving emails, close the IMAP connection:
imap_connection.close()
imap_connection.logout()
