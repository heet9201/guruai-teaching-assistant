# agents/sahayak_coordinator/agent.py
import os
import sys
from vertexai.generative_models import GenerativeModel, GenerationConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from agents.content_generator.agent import content_generator_agent

class GuruAICoordinator:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.instruction = """You are GuruAI, an intelligent teaching assistant for multi-grade 
        Indian classrooms. Route requests to appropriate specialists:
        
        - Hyper-local content creation → content_generator
        - Textbook image processing → worksheet_processor  
        
        Always respond in the teacher's preferred language and consider rural 
        Indian educational context."""
        
        self.config = GenerationConfig(
            temperature=0.5,
            max_output_tokens=1024
        )
        
        self.sub_agents = {
            "content_generator": content_generator_agent,
            # "worksheet_processor": worksheet_agent,
            # "knowledge_assistant": knowledge_agent,
            # "visual_designer": visual_agent,
            # "assessment_planner": assessment_agent
        }
    
    def generate_content(self, prompt, context=None):
        # Combine instruction with prompt
        full_prompt = f"{self.instruction}\n\nQuery: {prompt}"
        if context and "preferred_language" in context:
            full_prompt += f"\nPreferred Language: {context['preferred_language']}"
            
        return self.model.generate_content(
            full_prompt,
            generation_config=self.config
        )

# Create singleton instance
guruai_coordinator = GuruAICoordinator()
root_agent = guruai_coordinator

# - Student questions & explanations → knowledge_assistant
# - Visual aids & diagrams → visual_designer
# - Assessment & lesson planning → assessment_planner