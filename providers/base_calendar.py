class CalendarProvider:
    """Abstract base class for all calendar providers."""
    
    def authenticate(self):
        raise NotImplementedError("Subclasses must implement authenticate()")

    def fetch_events(self):
        raise NotImplementedError("Subclasses must implement fetch_events()")
