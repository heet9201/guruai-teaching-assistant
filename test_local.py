import os
from vertexai import init
from agents.guruai_coordinator.agent import root_agent

# Initialize Vertex AI
init(
    project="sahayak-demo-project",
    location="us-central1"
)

def test_agent():
    response = root_agent.generate_content(
        "What is 2+2?",
        context={"preferred_language": "english"}
    )
    print("Response:", response.text)

if __name__ == "__main__":
    test_agent() 