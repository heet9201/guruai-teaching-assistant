# GuruAI Teaching Assistant

An intelligent teaching assistant for multi-grade Indian classrooms that provides localized content generation, worksheet processing, and educational support.

## Project Overview

GuruAI is a multi-agent system that includes:

- **Coordinator Agent**: Routes requests to specialized agents
- **Content Generator**: Creates hyper-local educational content
- **Worksheet Processor**: Handles textbook image processing
- (Planned) Knowledge Assistant, Visual Designer, and Assessment Planner

## Prerequisites

- Python 3.8+
- Google Cloud account
- GitHub account
- Docker installed locally (for testing)

## Local Development Setup

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

## Deployment to Cloud Run

### 1. Initial Setup

1. Install Google Cloud SDK
2. Initialize Google Cloud:

```bash
gcloud init
gcloud auth configure-docker
```

3. Enable required APIs:

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com
```

### 2. Create Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
CMD exec gunicorn --bind :$PORT main:app
```

### 3. Create Cloud Run Service

1. Create a `main.py` file for the Flask application
2. Set up environment variables in Cloud Run
3. Deploy manually first to test:

```bash
gcloud run deploy guruai-assistant \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

### 4. GitHub Actions CI/CD Setup

1. Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

env:
  PROJECT_ID: your-project-id
  SERVICE_NAME: guruai-assistant
  REGION: asia-south1

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ env.PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}

      - name: Configure Docker
        run: gcloud auth configure-docker

      - name: Build and Push Image
        run: |
          docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA .
          docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy $SERVICE_NAME \
            --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
            --platform managed \
            --region $REGION \
            --allow-unauthenticated
```

### 5. Setup GitHub Secrets

1. Create a service account in Google Cloud Console
2. Download JSON key and add to GitHub repository secrets as `GCP_SA_KEY`
3. Grant required IAM roles:
   - Cloud Run Admin
   - Storage Admin
   - Service Account User

### 6. API Documentation

The service exposes the following endpoints:

- `POST /query`
  - Request body: `{"query": "your teaching question", "language": "preferred_language"}`
  - Response: JSON with agent response

Example usage:

```python
import requests

response = requests.post(
    "https://your-cloud-run-url/query",
    json={
        "query": "Create a lesson plan for grade 5 science",
        "language": "hindi"
    }
)
print(response.json())
```

## Environment Variables

Required environment variables:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key
- `PROJECT_ID`: Google Cloud project ID
- Other agent-specific configuration

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create pull request

## License

See [LICENSE](LICENSE) file.
