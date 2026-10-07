import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_google_meet_meeting(summary, start_time, duration_minutes=60, attendees=None):
    """
    Create a Google Meet meeting via Google Calendar API
    
    Args:
        summary: Meeting title
        start_time: datetime object for when the meeting starts
        duration_minutes: Length of meeting in minutes
        attendees: List of email addresses for attendees
        
    Returns:
        Meeting details including Google Meet link
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, let the user log in.
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

    service = build('calendar', 'v3', credentials=creds)
    
    # Calculate end time
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)
    
    # Format times for Google Calendar API
    start_str = start_time.isoformat()
    end_str = end_time.isoformat()
    
    # Prepare attendee list if provided
    attendee_list = []
    if attendees:
        attendee_list = [{'email': email} for email in attendees]
    
    # Create event with Google Meet conference
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_str,
            'timeZone': 'UTC',  # Adjust to your timezone
        },
        'end': {
            'dateTime': end_str,
            'timeZone': 'UTC',  # Adjust to your timezone
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f'meet-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
        'attendees': attendee_list
    }
    
    # Create the event with conference details
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()
    
    # Get the Google Meet link from the created event
    meet_link = event.get('hangoutLink', 'No Meet link created')
    
    return {
        'event_id': event['id'],
        'summary': event['summary'],
        'start_time': event['start']['dateTime'],
        'end_time': event['end']['dateTime'],
        'meet_link': meet_link,
        'attendees': [attendee.get('email') for attendee in event.get('attendees', [])]
    }

# Example usage
if __name__ == "__main__":
    # Create a meeting for tomorrow at 10:00 AM
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    meeting_time = datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 10, 0, 0
    )
    
    meeting = create_google_meet_meeting(
        summary="Project Status Meeting",
        start_time=meeting_time,
        duration_minutes=45,
        attendees=["colleague@example.com"]
    )
    
    print("Meeting created successfully!")
    print(f"Meeting link: {meeting['meet_link']}")