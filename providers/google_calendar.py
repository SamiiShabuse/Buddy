import datetime
import requests
import google_auth_oauthlib.flow
import google.auth.transport.requests
import google.oauth2.credentials
from .base_calendar import CalendarProvider  # Import base class

class GoogleCalendar(CalendarProvider):
    CLIENT_SECRETS_FILE = "client_secret.json"  # Path to your Google OAuth credentials file
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    TOKEN_FILE = "token.json"  # Stores the access token

    def __init__(self):
        self.credentials = None

    def authenticate(self):
        """Authenticates the user via Google's OAuth 2.0 interactive login."""
        try:
            # Load saved credentials if they exist
            self.credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(self.TOKEN_FILE)
        except Exception:
            self.credentials = None

        # If no valid credentials, prompt the user to log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(google.auth.transport.requests.Request())
            else:
                # Start the OAuth flow to get user authentication
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)

                # Save credentials for future use
                with open(self.TOKEN_FILE, "w") as token:
                    token.write(self.credentials.to_json())

        print("Authenticated successfully with Google Calendar!")

    def fetch_events(self, days=7):
        """Fetches events from Google Calendar."""
        if not self.credentials:
            raise Exception("You must authenticate first!")

        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        headers = {"Authorization": f"Bearer {self.credentials.token}"}
        params = {
            "timeMin": datetime.datetime.utcnow().isoformat() + "Z",
            "timeMax": (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z",
            "singleEvents": True,
            "orderBy": "startTime"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            events = response.json().get("items", [])
            print(f"Fetched {len(events)} events from Google Calendar.")
            return events
        else:
            raise Exception(f"Failed to fetch events: {response.text}")
