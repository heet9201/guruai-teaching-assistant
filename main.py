from flask import Flask, request, jsonify
from agents.guruai_coordinator.agent import root_agent
import os
from vertexai import init
from google.api_core import exceptions

app = Flask(__name__)

# Initialize Vertex AI
try:
    init(
        project=os.environ.get('GOOGLE_CLOUD_PROJECT'),
        location=os.environ.get('GOOGLE_CLOUD_LOCATION')
    )
except Exception as e:
    print(f"Warning: Failed to initialize Vertex AI: {str(e)}")

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
        try:
            response = root_agent.generate_content(
                prompt=query,
                context={"preferred_language": language}
            )
            
            return jsonify({
                "response": response.text,
                "language": language
            })
        except exceptions.PermissionDenied as e:
            return jsonify({
                "error": "Access to Vertex AI model denied. Please ensure Vertex AI API is enabled and you have necessary permissions.",
                "details": str(e)
            }), 403
        except exceptions.NotFound as e:
            return jsonify({
                "error": "Vertex AI model not found. Please ensure Gemini Pro model is enabled for your project.",
                "details": str(e)
            }), 404
        except Exception as e:
            return jsonify({
                "error": "Failed to generate response",
                "details": str(e)
            }), 500

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 