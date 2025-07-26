"""
Authentication module for GuruAI Teaching Assistant
Handles Firebase authentication and session management
"""

from .firebase_auth import initialize_firebase, verify_token, create_custom_token
from .session import initialize_session, get_session, set_session

__all__ = [
    "initialize_firebase",
    "verify_token",
    "create_custom_token",
    "initialize_session",
    "get_session",
    "set_session"
] 