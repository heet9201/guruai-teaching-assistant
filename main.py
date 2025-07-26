"""
GuruAI Teaching Assistant
Main application entry point
"""
import os
from dotenv import load_dotenv
from flask import Flask
from agents.auth import initialize_firebase, initialize_session
from agents.api import initialize_routes, initialize_middleware

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    
    # Initialize Firebase
    initialize_firebase()
    
    # Initialize session handling
    initialize_session(app)
    
    # Initialize routes and middleware
    initialize_routes(app)
    initialize_middleware(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8080)),
        debug=os.getenv('FLASK_ENV') == 'development'
    ) 