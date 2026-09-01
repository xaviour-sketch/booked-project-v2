import os
import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    if firebase_admin._apps:
        return

    credentials_path = os.environ.get("FIREBASE_CREDENTIALS")

    if not credentials_path:
        raise RuntimeError("FIREBASE_CREDENTIALS is not configured")

    if not os.path.isabs(credentials_path):
        credentials_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            credentials_path,
        )

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Firebase credentials file not found: {credentials_path}"
        )

    cred = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token):
    initialize_firebase()
    return auth.verify_id_token(id_token)
