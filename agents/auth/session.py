"""
Session Management Module for GuruAI Teaching Assistant
"""
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from flask import session
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

def initialize_session(app):
    """Initialize session handling for the Flask app"""
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.secret_key = app.config['SECRET_KEY']

def get_session(user_id: str, session_id: str) -> Optional[Dict]:
    """
    Retrieve session data from Firestore
    """
    try:
        doc_ref = db.collection('sessions').document(f"{user_id}_{session_id}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Error retrieving session: {str(e)}")
        return None

def set_session(user_id: str, session_id: str, data: Dict) -> bool:
    """
    Store session data in Firestore
    """
    try:
        # Add timestamp and TTL
        data['last_updated'] = datetime.utcnow()
        data['expires_at'] = datetime.utcnow() + timedelta(days=7)
        
        doc_ref = db.collection('sessions').document(f"{user_id}_{session_id}")
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        print(f"Error storing session: {str(e)}")
        return False

def create_conversation_session(user_id: str) -> str:
    """
    Create a new conversation session
    """
    try:
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'conversation_history': [],
            'context': {}
        }
        
        # Create a new document with auto-generated ID
        doc_ref = db.collection('sessions').document()
        session_id = doc_ref.id
        
        # Add session ID to the data and save
        session_data['session_id'] = session_id
        doc_ref.set(session_data)
        
        return session_id
    except Exception as e:
        print(f"Error creating conversation session: {str(e)}")
        raise

def add_to_conversation_history(user_id: str, session_id: str, message: Dict):
    """
    Add a message to the conversation history
    """
    try:
        doc_ref = db.collection('sessions').document(f"{user_id}_{session_id}")
        doc_ref.update({
            'conversation_history': firestore.ArrayUnion([{
                'timestamp': datetime.utcnow(),
                **message
            }]),
            'last_updated': datetime.utcnow()
        })
    except Exception as e:
        print(f"Error adding to conversation history: {str(e)}")
        raise 