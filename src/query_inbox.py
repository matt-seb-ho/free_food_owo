import base64
import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
  
# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
  
# email_bodies = []
def get_email_body(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message['payload']
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body_text = base64.urlsafe_b64decode(data).decode('utf-8')
                return body_text
    return None

def get_email_dict(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message['payload']
    subject = ""
    if 'headers' in payload:
        subject = [header['value'] for header in payload['headers'] if header['name'] == 'Subject'][0]

    best_part = None
    best_priority = None

    for part in message['payload']['parts']:
        if part['mimeType'] == 'multipart/alternative':
            for subpart in part['parts']:
                if subpart['mimeType'] == 'text/plain':
                    priority = subpart['headers'][0]['value']
                    if best_priority is None or priority < best_priority:
                        best_part = subpart
                        best_priority = priority
                    break
        elif part['mimeType'] == 'text/plain':
            priority = part['headers'][0]['value']
            if best_priority is None or priority < best_priority:
                best_part = part
                best_priority = priority

    # Decode the body from base64 and convert to plain text
    if best_part is not None:
        body = base64.urlsafe_b64decode(best_part['body']['data']).decode('utf-8')
    else:
        body = ""

    return {
        "subject": subject,
        "body": body 
    }


def get_emails(num_emails=10, query=None):
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("create new creds")

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("wrote to token")
  
    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
  
    # Query messages from inbox
    if query is not None:
        result = service.users().messages().list(maxResults=num_emails, userId='me', q=query).execute()
    else:
        result = service.users().messages().list(maxResults=num_emails, userId='me').execute()
    # messages is a list of dictionaries where each dictionary contains a message id.
    messages = result.get('messages')
  
    # iterate through all the messages
    # return {msg['id']: get_email_body(service, msg['id']) for msg in messages}
    return {msg['id']: get_email_dict(service, msg['id']) for msg in messages}
