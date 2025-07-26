"""
GuruAI Coordinator Agent
Manages and coordinates specialized educational agents
"""
from typing import Dict, Any, Optional, List
from vertexai.generative_models import GenerativeModel, GenerationConfig
from ..local_content_generator.agent import LocalContentGeneratorAgent
from ..knowledge_base.agent import KnowledgeBaseAgent
from ..visual_aid_generator.agent import VisualAidGeneratorAgent
from ..assessment_planner.agent import AssessmentPlannerAgent
from ..worksheet_processor.agent import WorksheetProcessorAgent

class GuruAICoordinator:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        
        # Initialize specialized agents
        self.content_generator = LocalContentGeneratorAgent()
        self.knowledge_base = KnowledgeBaseAgent()
        self.visual_aid_generator = VisualAidGeneratorAgent()
        self.assessment_planner = AssessmentPlannerAgent()
        self.worksheet_processor = WorksheetProcessorAgent()
        
        self.instruction = """You are GuruAI, an intelligent teaching assistant coordinator 
        for multi-grade Indian classrooms. Your role is to:

        1. Understand teacher requests and route to appropriate specialist agents
        2. Coordinate responses from multiple agents when needed
        3. Ensure consistent language and grade-level appropriate responses
        4. Maintain context and cultural relevance

        Available Specialists:
        - Local Content Generator: Creates culturally relevant stories and content
        - Knowledge Base: Provides simple explanations and analogies
        - Visual Aid Generator: Creates blackboard-friendly diagrams
        - Assessment & Planning: Handles assessments and lesson planning
        - Worksheet Processor: Creates differentiated worksheets
        """
        
        self.config = GenerationConfig(
            temperature=0.4,
            top_p=0.8,
            top_k=40
        )
    
    async def process_request(
        self,
        request: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process teacher request and coordinate appropriate responses"""
        try:
            # Extract request parameters
            intent = await self._determine_intent(request)
            language = context.get('language', 'english')
            grade_levels = context.get('grade_levels', ['5'])  # Default to grade 5
            
            # Route to appropriate agent(s)
            response = await self._route_request(
                intent=intent,
                request=request,
                language=language,
                grade_levels=grade_levels,
                context=context
            )
            
            return response
        
        except Exception as e:
            raise Exception(f"Error processing request: {str(e)}")
    
    async def process_textbook_image(
        self,
        image_data: bytes,
        grade_levels: List[str],
        subject: str = 'auto',
        language: str = 'hindi_english'
    ) -> Dict[str, Any]:
        """Process textbook image and generate worksheets"""
        try:
            return await self.worksheet_processor.process_image(
                image_data=image_data,
                grade_levels=grade_levels,
                subject=subject,
                language=language
            )
        
        except Exception as e:
            raise Exception(f"Error processing textbook image: {str(e)}")
    
    async def _determine_intent(self, request: str) -> Dict[str, Any]:
        """Determine the intent and required agents for the request"""
        try:
            response = await self.model.generate_content(
                f"""Analyze the following teacher request and determine required agents:
                Request: {request}
                
                Respond in JSON format with:
                1. primary_intent: Main purpose (content/knowledge/visual/assessment/worksheet)
                2. required_agents: List of needed specialist agents
                3. parameters: Any specific parameters identified
                """,
                generation_config=self.config
            )
            
            return eval(response.text)  # Convert string to dict
            
        except Exception as e:
            raise Exception(f"Error determining intent: {str(e)}")
    
    async def _route_request(
        self,
        intent: Dict[str, Any],
        request: str,
        language: str,
        grade_levels: List[str],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Route request to appropriate agent(s) and combine responses"""
        try:
            responses = {}
            
            # Route based on primary intent
            if intent['primary_intent'] == 'content':
                responses['content'] = await self.content_generator.generate_story(
                    topic=request,
                    language=language,
                    grade_level=grade_levels[0],
                    cultural_context=context.get('cultural_context')
                )
            
            elif intent['primary_intent'] == 'knowledge':
                responses['explanation'] = await self.knowledge_base.explain_concept(
                    question=request,
                    language=language,
                    grade_level=grade_levels[0]
                )
            
            elif intent['primary_intent'] == 'visual':
                responses['visual'] = await self.visual_aid_generator.create_diagram(
                    concept=request,
                    language=language,
                    grade_level=grade_levels[0]
                )
            
            elif intent['primary_intent'] == 'assessment':
                responses['assessment'] = await self.assessment_planner.create_lesson_plan(
                    subjects=[intent['parameters'].get('subject', 'general')],
                    grade_levels=grade_levels,
                    duration_days=intent['parameters'].get('duration', 5),
                    language=language
                )
            
            # Add responses from additional required agents
            for agent in intent.get('required_agents', []):
                if agent not in responses:
                    responses[agent] = await self._get_agent_response(
                        agent=agent,
                        request=request,
                        language=language,
                        grade_levels=grade_levels,
                        context=context
                    )
            
            return responses
        
        except Exception as e:
            raise Exception(f"Error routing request: {str(e)}")
    
    async def _get_agent_response(
        self,
        agent: str,
        request: str,
        language: str,
        grade_levels: List[str],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Get response from a specific agent"""
        try:
            if agent == 'content_generator':
                return await self.content_generator.generate_story(
                    topic=request,
                    language=language,
                    grade_level=grade_levels[0],
                    cultural_context=context.get('cultural_context')
                )
            
            elif agent == 'knowledge_base':
                return await self.knowledge_base.explain_concept(
                    question=request,
                    language=language,
                    grade_level=grade_levels[0]
                )
            
            elif agent == 'visual_aid_generator':
                return await self.visual_aid_generator.create_diagram(
                    concept=request,
                    language=language,
                    grade_level=grade_levels[0]
                )
            
            elif agent == 'assessment_planner':
                return await self.assessment_planner.create_lesson_plan(
                    subjects=[context.get('subject', 'general')],
                    grade_levels=grade_levels,
                    language=language
                )
            
            else:
                raise ValueError(f"Unknown agent: {agent}")
        
        except Exception as e:
            raise Exception(f"Error getting agent response: {str(e)}")