from flask import Flask, request, jsonify
from agents.guruai_coordinator.agent import root_agent
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({"status": "healthy"}), 200

@app.route('/query', methods=['POST'])
def handle_query():
    """Main endpoint to handle teaching assistant queries"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing required field: query"
            }), 400

        query = data['query']
        language = data.get('language', 'english')  # Default to English if not specified
        
        # Get response from GuruAI coordinator
        response = root_agent.generate_content(
            prompt=query,
            context={"preferred_language": language}
        )
        
        return jsonify({
            "response": response.text,
            "language": language
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 