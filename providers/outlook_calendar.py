import requests
import msal
import datetime
from .base_calendar import CalendarProvider  # Import base class

class OutlookCalendar(CalendarProvider):
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    TENANT_ID = "your_tenant_id"
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["https://graph.microsoft.com/.default"]

    def __init__(self):
        self.access_token = None

    def authenticate(self):
        """Authenticates with Microsoft Graph API."""
        app = msal.ConfidentialClientApplication(
            self.CLIENT_ID, authority=self.AUTHORITY, client_credential=self.CLIENT_SECRET
        )
        token_response = app.acquire_token_for_client(scopes=self.SCOPES)
        
        if "access_token" in token_response:
            self.access_token = token_response["access_token"]
            print("Authenticated with Outlook Calendar!")
        else:
            raise Exception(f"Authentication failed: {token_response.get('error_description', 'Unknown error')}")

    def fetch_events(self, days=7):
        """Fetches events from Outlook Calendar."""
        if not self.access_token:
            raise Exception("You must authenticate first!")

        url = "https://graph.microsoft.com/v1.0/me/calendar/events"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "$filter": f"start/dateTime ge '{datetime.datetime.utcnow().isoformat()}Z' "
                       f"and end/dateTime le '{(datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()}Z'"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            events = response.json().get("value", [])
            print(f"Fetched {len(events)} events from Outlook Calendar.")
            return events
        else:
            raise Exception(f"Failed to fetch events: {response.text}")
