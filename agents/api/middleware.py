"""
API Middleware for GuruAI Teaching Assistant
"""
from flask import request, g
from functools import wraps
import time

def initialize_middleware(app):
    """Initialize API middleware"""
    
    @app.before_request
    def before_request():
        """Actions to perform before each request"""
        g.start_time = time.time()
        
        # Add request ID for tracking
        g.request_id = request.headers.get('X-Request-ID') or str(time.time())
        
        # Initialize context for the request
        g.context = {
            'request_id': g.request_id,
            'user_id': None,  # Will be set by auth middleware
            'session_id': None  # Will be set by session middleware
        }
    
    @app.after_request
    def after_request(response):
        """Actions to perform after each request"""
        # Calculate request duration
        duration = time.time() - g.start_time
        
        # Add custom headers
        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-Response-Time'] = str(duration)
        
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Global exception handler"""
        # Log the error with request context
        app.logger.error(f"Error processing request {g.request_id}: {str(e)}")
        
        # Return appropriate error response
        return {
            'error': 'Internal server error',
            'request_id': g.request_id
        }, 500 