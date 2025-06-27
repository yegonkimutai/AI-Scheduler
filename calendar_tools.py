import json
from google_apis import create_service

client_secret = 'client_secret.json'

def construct_google_calendar_client(client_secret):
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)
    return service

calendar_service = construct_google_calendar_client(client_secret)

def create_calendar_list(calendar_name):
    calendar_list = {
        'summary': calendar_name
    }
    created_calendar_list = calendar_service.calendarList().insert(body=calendar_list).execute()
    return created_calendar_list

def list_calendar_list(max_capacity=200):
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)

    all_calendars = []
    all_calendars_cleaned = []
    next_page_token = None
    capacity_tracker = 0

    while True:
        calendar_list = calendar_service.calendarList().list(
            maxResults = min(200, max_capacity - capacity_tracker),
            pageToken = next_page_token
        ).execute()
        calendars = calendar_list.get('items', [])
        all_calendars.extend(calendars)
        capacity_tracker += len(calendars)
        if capacity_tracker >= max_capacity:
            break
        next_page_token = calendar_list.get('nextPageToken')
        if not next_page_token:
            break

        for calendar in all_calendars:
            all_calendars_cleaned.append(
                {
                    'id': calendar['id'],
                    'name': calendar['summary'],
                    'description': calendar.get('description', '')
                })
        return all_calendars_cleaned

def list_calendar_events(calendar_id, max_capacity=20):
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)

    all_events = []
    next_page_token = None
    capacity_tracker = 0

    while True:
        events_list = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults = min(250, max_capacity - capacity_tracker),
            pageToken = next_page_token
        ).execute()
        events = events_list.get('items', [])
        all_events.extend(events)
        capacity_tracker += len(events)
        if capacity_tracker >= max_capacity:
            break
        next_page_token = events_list.get('nextPageToken')
        if not next_page_token:
            break
    return all_events

def insert_calendar_event(calendar_id, **kwargs):
    request_body = json.loads(kwargs['kwargs'])
    event = calendar_service.events().insert(
        calendar_id=calendar_id,
        body=request_body
    ).execute()
    return event
