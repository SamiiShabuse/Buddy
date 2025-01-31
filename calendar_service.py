from abc import ABC, staticmethod

class CalendarProvider:
    def authenticate(self):
        """Handles authentication for the calendar API."""
        raise NotImplementedError

    def fetch_events(self):
        """Fetches events from the calendar API."""
        raise NotImplementedError


class GoogleCalendar(CalendarProvider):
    def authenticate(self):
        print("Authenticating with Google Calendar...")

    def fetch_events(self):
        print("Fetching events from Google Calendar...")


class OutlookCalendar(CalendarProvider):
    def authenticate(self):
        print("Authenticating with Outlook Calendar...")

    def fetch_events(self):
        print("Fetching events from Outlook Calendar...")