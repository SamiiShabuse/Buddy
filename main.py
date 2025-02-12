from fastapi import FastAPI
from google.cloud import firestore
import json

# Initialize FastAPI app
app = FastAPI()

# Load Firebase credentials
firebase_key_path = "firebase-key.json"
db = firestore.Client.from_service_account_json(firebase_key_path)

# 📌 Test Route
@app.get("/")
def read_root():
    return {"message": "FastAPI + Firebase is working!"}

# 📌 Save Data to Firestore
@app.post("/add-event/")
def add_event(event_id: str, title: str):
    doc_ref = db.collection("events").document(event_id)
    doc_ref.set({"title": title})
    return {"message": f"Event {title} added successfully!"}

# 📌 Get Data from Firestore
@app.get("/get-events/")
def get_events():
    events_ref = db.collection("events").stream()
    events = {doc.id: doc.to_dict() for doc in events_ref}
    return events

