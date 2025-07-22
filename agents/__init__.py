# agents/__init__.py
"""
Sahayak Teaching Assistant Multi-Agent System
Built with Google ADK for multi-grade classroom support in India
"""

from .guruai_coordinator.agent import guruai_coordinator as root_agent
from .content_generator.agent import content_generator_agent
from .worksheet_processor.agent import worksheet_processor_agent  
# from .knowledge_assistant.agent import knowledge_assistant_agent
# from .visual_designer.agent import visual_designer_agent
# from .assessment_planner.agent import assessment_planner_agent

__all__ = [
    "root_agent",
    "content_generator_agent",
    "worksheet_processor_agent", 
    # "knowledge_assistant_agent",
    # "visual_designer_agent",
    # "assessment_planner_agent"
]

__version__ = "1.0.0"
__author__ = "GuruAI Team"
__description__ = "AI teaching assistant for multi-grade Indian classrooms"
