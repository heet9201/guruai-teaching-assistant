"""
API Module for GuruAI Teaching Assistant
Handles authenticated endpoints and request routing
"""

from .routes import initialize_routes
from .middleware import initialize_middleware

__all__ = [
    "initialize_routes",
    "initialize_middleware"
] 