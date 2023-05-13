from __future__ import print_function

import datetime
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

    if "end" in event:
        end = event["end"]
    else:
        end = (datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.000') + datetime.timedelta(hours = 1)).isoformat()
        
    cal_event = {
        'summary' : f'Free Food at {event_name}',
        'location' : '',
        'description': f'There will be free food at {location}',
        'start' : {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
        },
        'end' : {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles',
        }
    }
    
    return cal_event

def create_event(new_event, max_events = 10, days_ago=10):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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
        today = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming few events')
        events_result = service.events().list(calendarId='primary', timeMin=today,
                                              maxResults=max_events, singleEvents=True,
                                              orderBy='startTime').execute()
        event_list = events_result.get('items', [])
        event_name = [event_list[i]['summary'] for i in range(len(event_list))]
        # create events from events

        if new_event['summary'] not in event_name:
            event = service.events().insert(calendarId='primary', body=new_event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

        # Prints the start and name of the next 10 events
        for event in event_list:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


events = [{
    'summary': f'[Free Food] pizza at lmao!!',
    'location': '',
    'description': f'There will be free food at ',
    'start': { 
        'dateTime': "2023-05-12T13:00:00.000Z", # YYYY-MM-DDThh:mm:ss+00:00
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': "2023-05-12T15:00:00.000Z",
        'timeZone': 'America/Los_Angeles',
    },
    },{
    'summary': f'[Free Food] donuts at 190a class',
    'location': '',
    'description': f'There will be free food at somwhere',
    'start': { 
        'dateTime': "2023-05-15T12:00:00", # YYYY-MM-DDThh:mm:ss+00:00
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': "2023-05-15T14:00:00",
        'timeZone': 'America/Los_Angeles',
    },
    },{
    'summary': f'[Free Food] free foods at midnight event thing',
    'location': '',
    'description': f'There will be free food at dunno',
    'start': { 
        'dateTime': "2023-05-20T20:00:00", # YYYY-MM-DDThh:mm:ss+00:00
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': "2023-05-21T04:00:00",
        'timeZone': 'America/Los_Angeles',
    },
    }, ]


if __name__ == '__main__':
    event_json = {
        "name": "HRL Laboratories Professionalism Workshop",
        "start": "2023-05-11T18:00:00.000",
        "end": "2023-05-11T19:00:000",
        "location": "ESB 1001"
    }
    e = convert_json(event_json)
    create_event(e)