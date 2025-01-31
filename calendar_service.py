from providers.outlook_calendar import OutlookCalendar

def main():
    outlook = OutlookCalendar()
    outlook.authenticate()
    events = outlook.fetch_events()
    print(events)

if __name__ == "__main__":
    main()
