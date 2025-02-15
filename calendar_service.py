from providers.outlook_calendar import OutlookCalendar
from providers.google_calendar import GoogleCalendar

def main():
    print("Choose a calendar provider:")
    print("1. Outlook")
    print("2. Google")
    
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        calendar = OutlookCalendar()
    elif choice == "2":
        calendar = GoogleCalendar()
    else:
        print("Invalid choice. Exiting.")
        return

    # Authenticate user
    calendar.authenticate()
    
    # Fetch events
    events = calendar.fetch_events()
    
    # Print events
    print(events)

if __name__ == "__main__":
    main()
