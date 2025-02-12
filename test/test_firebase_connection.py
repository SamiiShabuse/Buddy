from fastapi import FastAPI
from google.cloud import firestore
import uuid  # To generate unique user IDs

# Initialize FastAPI app
app = FastAPI()

# Load Firebase credentials
firebase_key_path = "config/firebase-key.json"
db = firestore.Client.from_service_account_json(firebase_key_path)

# 📌 Add a new user to Firestore
@app.post("/add-user/")
def add_user(name: str, email: str):
    user_id = str(uuid.uuid4())  # Generate a unique user ID
    doc_ref = db.collection("users").document(user_id)  # Store in 'users' collection
    doc_ref.set({
        "name": name,
        "email": email
    })
    return {"message": f"User {name} added successfully!", "user_id": user_id}

# 📌 Fetch all users from Firestore
@app.get("/get-users/")
def get_users():
    users_ref = db.collection("users").stream()
    users = {doc.id: doc.to_dict() for doc in users_ref}
    return users
