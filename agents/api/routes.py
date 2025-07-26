"""
API Routes for GuruAI Teaching Assistant
"""
from flask import Blueprint, request, jsonify
from ..auth.firebase_auth import require_auth
from ..auth.session import (
    create_conversation_session,
    get_session,
    add_to_conversation_history
)
from ..guruai_coordinator.agent import GuruAICoordinator

api = Blueprint('api', __name__)
coordinator = GuruAICoordinator()

def initialize_routes(app):
    """Initialize API routes"""
    app.register_blueprint(api, url_prefix='/api/v1')

@api.route('/sessions', methods=['POST'])
@require_auth
def create_session():
    """Create a new conversation session"""
    try:
        user_id = request.user['uid']
        session_id = create_conversation_session(user_id)
        return jsonify({
            'session_id': session_id,
            'message': 'Session created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/sessions/<session_id>', methods=['GET'])
@require_auth
def get_session_history(session_id):
    """Get conversation history for a session"""
    try:
        user_id = request.user['uid']
        session_data = get_session(user_id, session_id)
        if not session_data:
            return jsonify({'error': 'Session not found'}), 404
        return jsonify(session_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/chat/<session_id>', methods=['POST'])
@require_auth
def chat(session_id):
    """Handle chat messages"""
    try:
        user_id = request.user['uid']
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
            
        # Get user's message
        user_message = data['message']
        context = data.get('context', {})
        
        # Add user message to history
        add_to_conversation_history(user_id, session_id, {
            'role': 'user',
            'content': user_message
        })
        
        # Process with coordinator
        response = coordinator.generate_content(
            prompt=user_message,
            context=context
        )
        
        # Add assistant response to history
        add_to_conversation_history(user_id, session_id, {
            'role': 'assistant',
            'content': response
        })
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/process-image/<session_id>', methods=['POST'])
@require_auth
def process_image(session_id):
    """Process textbook images for worksheet generation"""
    try:
        user_id = request.user['uid']
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        grade_levels = request.form.getlist('grade_levels')
        subject = request.form.get('subject', 'auto')
        language = request.form.get('language', 'hindi_english')
        
        # Process image and generate worksheets
        worksheets = coordinator.process_textbook_image(
            image_file,
            grade_levels,
            subject,
            language
        )
        
        # Add to session history
        add_to_conversation_history(user_id, session_id, {
            'role': 'system',
            'content': 'Processed textbook image and generated worksheets',
            'worksheets': worksheets
        })
        
        return jsonify({
            'worksheets': worksheets,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 