# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
food = "pizza"
event = "lmao"
location = ""
start_time = "2015-05-28T09:00:00"
end_time = "2015-05-28T09:00:00"
time_zone = ""

event = {
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
}

event = service.events().insert(calendarId='primary', body=event).execute()
print 'Event created: %s' % (event.get('htmlLink'))
