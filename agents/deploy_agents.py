import os
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from guruai_coordinator.agent import root_agent

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT","sahayak-demo-project"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION","us-central1"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_STAGING_BUCKET","gs://guruai-teaching-assistant")
)

# app = reasoning_engines.AdkApp(
#     agent=root_agent,
#     enable_tracing=True,
# )
# remote_app = agent_engines.create(
#     root_agent,
#     requirements=[
#       "google-cloud-aiplatform[adk,agent_engines]",
#       # add any other pip dependencies
#     ],
#     env_vars={
#       "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY","AIzaSyDTzsrV_7NwO8c0goEZpesxcRrPot389zY"),
#       # "OTHER_ENV": "<value>"
#     }
# )
# print(f"Deployed agent endpoint: {remote_app.resource_name}")

# Redeploy the agent after fixing potential issues
try:
    remote_app = agent_engines.create(
        agent_engine=root_agent,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]"
        ],
        env_vars={
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY","AIzaSyDTzsrV_7NwO8c0goEZpesxcRrPot389zY"),
        }
    )
    print("Agent redeployed successfully:", remote_app)
    print(f"Deployed agent endpoint: {remote_app.resource_name}")
except Exception as e:
    print(f"Failed to redeploy agent: {e}")
