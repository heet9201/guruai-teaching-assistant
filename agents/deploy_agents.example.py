import os
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from guruai_coordinator.agent import root_agent

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "your-location"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_STAGING_BUCKET", "your-staging-bucket")
)

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

try:
    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]"
        ],
        extra_packages=["./agents/content_generator", "./agents/worksheet_processor"],
        env_vars={
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", "your-google-api-key"),
        }
    )
    print("Agent redeployed successfully:", remote_app)
except Exception as e:
    print(f"Failed to redeploy agent: {e}")
