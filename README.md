# GuruAI Teaching Assistant

An AI-powered teaching assistant for multi-grade Indian classrooms that helps teachers create localized content, differentiated materials, and manage diverse learning environments.

## Features

1. **Hyper-Local Content Generation**

   - Create stories in local languages
   - Culturally relevant examples
   - Multi-grade adaptations

2. **Differentiated Materials**

   - Process textbook images
   - Generate grade-specific worksheets
   - Support multiple languages

3. **Knowledge Base**

   - Simple explanations for complex topics
   - Local language support
   - Grade-appropriate analogies

4. **Visual Aids**

   - Blackboard-friendly diagrams
   - Simple charts and graphs
   - Multi-language labels

5. **Assessment & Planning**
   - Audio-based reading assessments
   - Weekly lesson planning
   - Educational game generation

## Setup

### Prerequisites

1. Python 3.10 or higher
2. Google Cloud account with the following APIs enabled:
   - Vertex AI
   - Cloud Vision
   - Cloud Translation
   - Cloud Speech-to-Text
3. Firebase account and project

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/guruai-teaching-assistant.git
   cd guruai-teaching-assistant
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Firebase Setup

1. Install Firebase CLI:

   ```bash
   npm install -g firebase-tools
   ```

2. Login to Firebase:

   ```bash
   firebase login
   ```

3. Initialize Firebase project:

   ```bash
   firebase init
   ```

4. Deploy to Firebase:
   ```bash
   firebase deploy
   ```

## API Usage

### Authentication

All API endpoints require Firebase authentication. Include the Firebase ID token in the Authorization header:

```http
Authorization: Bearer <firebase-id-token>
```

### Endpoints

1. Create Session

```http
POST /api/v1/sessions
Response: {
    "session_id": "session-uuid",
    "message": "Session created successfully"
}
```

2. Chat

```http
POST /api/v1/chat/<session_id>
Content-Type: application/json

{
    "message": "Create a story in Marathi about farmers",
    "context": {
        "language": "marathi",
        "grade_levels": ["3", "4"],
        "subject": "science"
    }
}
```

3. Process Image

```http
POST /api/v1/process-image/<session_id>
Content-Type: multipart/form-data

image: <file>
grade_levels: ["3", "4", "5"]
subject: science
language: hindi_english
```

### Example Usage

1. Generate Local Content:

```python
import requests

response = requests.post(
    "https://your-app.web.app/api/v1/chat/session-id",
    headers={
        "Authorization": f"Bearer {firebase_token}"
    },
    json={
        "message": "Create a story in Marathi about water cycle",
        "context": {
            "language": "marathi",
            "grade_levels": ["4"],
            "subject": "science"
        }
    }
)
```

2. Process Textbook Image:

```python
import requests

with open("textbook_page.jpg", "rb") as f:
    response = requests.post(
        "https://your-app.web.app/api/v1/process-image/session-id",
        headers={
            "Authorization": f"Bearer {firebase_token}"
        },
        files={
            "image": f
        },
        data={
            "grade_levels": ["3", "4", "5"],
            "subject": "mathematics",
            "language": "hindi_english"
        }
    )
```

## Development

### Project Structure

```
guruai-teaching-assistant/
├── agents/
│   ├── local_content_generator/
│   ├── knowledge_base/
│   ├── visual_aid_generator/
│   ├── assessment_planner/
│   └── worksheet_processor/
├── api/
│   └── routes.py
├── auth/
│   ├── firebase_auth.py
│   └── session.py
└── main.py
```

### Adding New Features

1. Create new agent in `agents/` directory
2. Update coordinator in `agents/guruai_coordinator/agent.py`
3. Add API endpoints in `agents/api/routes.py`
4. Update tests and documentation

### Testing

Run tests:

```bash
pytest
```

### Local Development

1. Start Firebase emulators:

```bash
firebase emulators:start
```

2. Run development server:

```bash
FLASK_ENV=development flask run
```

## Deployment

1. Build and test:

```bash
pytest
black .
flake8
```

2. Deploy to Firebase:

```bash
firebase deploy
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
