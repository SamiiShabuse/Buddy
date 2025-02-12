from fastapi import FastAPI
from google.cloud import firestore
import uuid  # To generate unique user IDs
from providers.outlook_calendar import OutlookCalendar
from providers.google_calendar import GoogleCalendar

# Initialize FastAPI app
app = FastAPI()

# Load Firebase credentials
firebase_key_path = "config/firebase-key.json"
db = firestore.Client.from_service_account_json(firebase_key_path)

# 📌 Add a new user to Firestore
@app.post("/add-user/")
def add_user(name: str, email: str, calendar_type: str):
    user_id = str(uuid.uuid4())  # Generate a unique user ID
    doc_ref = db.collection("users").document(user_id)  # Store in 'users' collection
    doc_ref.set({
        "name": name,
        "email": email,
        "calendar_type": calendar_type,  # Store their selected calendar type
        "events": []  # Placeholder for storing calendar events
    })
    return {"message": f"User {name} added successfully!", "user_id": user_id}

# 📌 Fetch user's events from their calendar and save to Firestore
@app.get("/fetch-events/{user_id}/")
def fetch_and_store_events(user_id: str):
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()

    if not user.exists:
        return {"error": "User not found"}

    user_data = user.to_dict()
    calendar_type = user_data.get("calendar_type")

    # Choose the correct calendar provider
    if calendar_type == "Outlook":
        calendar = OutlookCalendar()
    elif calendar_type == "Google":
        calendar = GoogleCalendar()
    else:
        return {"error": "Invalid calendar type"}

    # Authenticate user
    calendar.authenticate()

    # Fetch events
    events = calendar.fetch_events()

    # Store events in Firestore under the user's document
    user_ref.update({"events": events})

    return {"message": "Events fetched and stored successfully", "events": events}

# 📌 Fetch all users from Firestore
@app.get("/get-users/")
def get_users():
    users_ref = db.collection("users").stream()
    users = {doc.id: doc.to_dict() for doc in users_ref}
    return users
