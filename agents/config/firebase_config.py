"""
Firebase Configuration Module
Handles Firebase initialization and configuration
"""
import os
from firebase_admin import initialize_app, credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Get the service account key path from environment variable
        service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
        
        if not service_account_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH environment variable not set")
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(service_account_path)
        firebase_app = initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
            'databaseURL': os.getenv('FIREBASE_DATABASE_URL', None)
        })
        
        print("Firebase initialized successfully")
        return firebase_app
        
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        raise 