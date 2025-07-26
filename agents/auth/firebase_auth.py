"""
Firebase Authentication Module for GuruAI Teaching Assistant
"""
import os
from typing import Dict, Optional
import firebase_admin
from firebase_admin import auth, credentials
from functools import wraps
from flask import request, jsonify

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    cred = credentials.Certificate(
        os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
    )
    firebase_admin.initialize_app(cred)

def verify_token(token: str) -> Optional[Dict]:
    """Verify Firebase ID token and return decoded claims"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None

def create_custom_token(uid: str, claims: Dict = None) -> str:
    """Create a custom token for a user with optional claims"""
    try:
        return auth.create_custom_token(uid, claims)
    except Exception as e:
        raise ValueError(f"Error creating custom token: {str(e)}")

def require_auth(f):
    """Decorator to require Firebase authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split('Bearer ')[1]
        decoded_token = verify_token(token)
        
        if not decoded_token:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Add user info to request
        request.user = decoded_token
        return f(*args, **kwargs)
    
    return decorated_function 