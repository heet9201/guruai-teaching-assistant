# agents/sahayak_coordinator/agent.py
from google.adk.agents import LlmAgent
from google.genai import types
# from ..content_generator.agent import content_generator_agent

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from agents.content_generator.agent import content_generator_agent

# from ..worksheet_processor.agent import worksheet_agent
# from ..knowledge_assistant.agent import knowledge_agent
# from ..visual_designer.agent import visual_agent
# from ..assessment_planner.agent import assessment_agent

guruai_coordinator = LlmAgent(
    name="guruai_coordinator",
    model="gemini-2.0-flash",
    instruction="""You are GuruAI, an intelligent teaching assistant for multi-grade 
    Indian classrooms. Route requests to appropriate specialists:
    
    - Hyper-local content creation → content_generator
    - Textbook image processing → worksheet_processor  
    
    Always respond in the teacher's preferred language and consider rural 
    Indian educational context.""",
    sub_agents=[
        content_generator_agent,
        # worksheet_agent,
        # knowledge_agent,
        # visual_agent,
        # assessment_agent
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=1024
    )
)

# Export for backend integration
root_agent = guruai_coordinator

# - Student questions & explanations → knowledge_assistant
# - Visual aids & diagrams → visual_designer
# - Assessment & lesson planning → assessment_planner