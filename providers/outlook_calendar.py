import requests
import msal
import datetime
from .base_calendar import CalendarProvider  # Import base class

class OutlookCalendar(CalendarProvider):
    CLIENT_ID = "your_client_id"
    TENANT_ID = "your_tenant_id"
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

    #Required for us to read the calendar 
    SCOPES = ["User.Read", "Calendars.Read"] 
    REDIRECT_URI = "http://localhost"  # Must match what's set in Azure AD

    def __init__(self):
        self.access_token = None

    def authenticate(self):
        """Authenticates the user via interactive login."""
        app = msal.PublicClientApplication(self.CLIENT_ID, authority=self.AUTHORITY)

        # Attempt to get a token silently (useful if the user is already logged in)
        accounts = app.get_accounts()
        if accounts:
            token_response = app.acquire_token_silent(self.SCOPES, account=accounts[0])
        else:
            # If no cached token, prompt the user to log in
            token_response = app.acquire_token_interactive(self.SCOPES, redirect_uri=self.REDIRECT_URI)

        if "access_token" in token_response:
            self.access_token = token_response["access_token"]
            print("Authenticated successfully with Outlook Calendar!")
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
