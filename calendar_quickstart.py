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

food ="pizza"
event = "lmao"
location = ""
start_time = "2023-05-28T07:00:00"
end_time = "2023-05-28T09:00:00"
time_zone = ""

events = [{
  'summary': f'[Free Food] {food} at {event}',
  'location': '',
  'description': f'There will be free food at {location}',
  'start': { 
    'dateTime': start_time, # YYYY-MM-DDThh:mm:ss+00:00
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': end_time,
    'timeZone': 'America/Los_Angeles',
  },
},{
  'summary': f'[Free Food] donuts at 190a class',
  'location': '',
  'description': f'There will be free food at {location}',
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

def main():
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
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        event_list = events_result.get('items', [])
        event_names = [event_list[i]['summary'] for i in range(len(event_list))]
        # create events from events
        
        for e in events:
            if e['summary'] not in event_names:
                event = service.events().insert(calendarId='primary', body=e).execute()
                print('Event created: %s' % (event.get('htmlLink')))

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in event_list:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()