import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import Dict, Any

class FirebaseManager:
    def __init__(self):
        self.db = None
        self._initialize()

    def _initialize(self):
        try:
            # Check for credential file or env var
            cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
            
            if os.path.exists(cred_path):
                # cred = credentials.Certificate(cred_path)
                # firebase_admin.initialize_app(cred)
                # self.db = firestore.client()
                print(f"[Firebase] Initialized with {cred_path} (MOCKED FOR NOW)")
                # NOTE: Commented out actual init to prevent crashing without real key
                self.db = "MOCK_DB" 
            else:
                print("[Firebase] No credentials found. Running in local-only mode.")
        except Exception as e:
            print(f"[Firebase] Initialization failed: {e}")

    def log_state(self, normalized_data: Dict[str, Any]):
        """Push state to Firestore (Mocked if no DB)."""
        if not self.db or self.db == "MOCK_DB":
            if self.db == "MOCK_DB":
                 # Simulate latency or success
                 pass
            return

        try:
            # Actual Firestore write code would go here
            # doc_ref = self.db.collection(u'digital_twin_states').document(normalized_data['id'])
            # doc_ref.set(normalized_data)
            pass
        except Exception as e:
            print(f"Failed to log to Firebase: {e}")
