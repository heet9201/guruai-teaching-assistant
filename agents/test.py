import requests
import json
from google.auth.transport.requests import Request
from google.auth import jwt

# The URL of the endpoint (from Google Cloud Console)
url = "https://us-central1-aiplatform.googleapis.com/v1/projects/sahayak-demo-project/locations/us-central1/endpoints/your_endpoint_id:predict"

# Get the token to authenticate the API request
credentials = jwt.Credentials.from_service_account_file('/path/to/your-service-account-key.json')
auth_request = Request()
token = credentials.refresh(auth_request).token

# Prepare your payload (input data for the model)
data = {
    "instances": [
        {"input_field": "value"}
    ]
}

# Headers including the access token for authorization
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Make the POST request to Vertex AI endpoint
response = requests.post(url, json=data, headers=headers)

# Print the response
print(response.json())
