import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def convert_json(event):
    event_name = event["name"]
    location = event["location"]
    start = event["start"]
    cal_event = {
        'summary' : f'Free Food at {event_name}',
        'location' : '',
        'description': f'There will be free food at {location}.',
        'start' : {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
        },
        'end' : {
            'dateTime': event['end'],
            'timeZone': 'America/Los_Angeles',
        }
    }
    
    return cal_event

def create_event(new_event):
    """
    add event to calendar

    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        event = service.events().insert(calendarId='primary', body=new_event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return True

    except HttpError as error:
        print('An error occurred: %s' % error)
        return False


"""
# TESTING 
if __name__ == '__main__':
    event_json = {
        "name": "HRL Laboratories Professionalism Workshop",
        "start": "2023-05-11T18:00:00.000",
        "end": "2023-05-11T19:00:000",
        "location": "ESB 1001"
    }
    e = convert_json(event_json)
    create_event(e)

"""
