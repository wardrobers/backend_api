import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def verify_id_token(id_token):
    try:
        # Verify the ID token and decode its payload
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except ValueError as exc:
        # Token is invalid
        raise HTTPException(status_code=401, detail="Invalid token") from exc
