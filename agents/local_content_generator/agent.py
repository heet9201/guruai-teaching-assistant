"""
Local Content Generator Agent
Specializes in creating culturally relevant educational content in local languages
"""
from typing import Dict, Any, Optional
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import translate_v2 as translate
from .tools import (
    generate_local_story,
    create_cultural_analogies,
    translate_content,
    get_cultural_context
)

class LocalContentGeneratorAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.translate_client = translate.Client()
        
        self.instruction = """You are an expert educational content creator specializing in 
        Indian regional contexts. Your role is to generate engaging, culturally relevant 
        educational content in local languages.

        Key Capabilities:
        1. Create stories and examples using local cultural elements
        2. Generate content in multiple Indian languages
        3. Adapt content for different grade levels
        4. Ensure cultural authenticity and sensitivity

        Always consider:
        - Local customs and traditions
        - Regional agricultural practices
        - Local festivals and celebrations
        - Common daily life experiences
        - Regional history and geography
        """
        
        self.config = GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40
        )
    
    async def generate_story(
        self,
        topic: str,
        language: str,
        grade_level: str,
        cultural_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate a culturally relevant story"""
        try:
            # Get cultural context if not provided
            if not cultural_context:
                cultural_context = await get_cultural_context(language)
            
            # Generate story in English first
            story = await generate_local_story(
                topic=topic,
                cultural_context=cultural_context,
                grade_level=grade_level,
                model=self.model,
                config=self.config
            )
            
            # Translate to target language if not English
            if language.lower() != 'english':
                story = await translate_content(
                    content=story,
                    target_language=language,
                    translate_client=self.translate_client
                )
            
            return {
                'content': story,
                'language': language,
                'topic': topic,
                'grade_level': grade_level,
                'cultural_context': cultural_context
            }
        
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")
    
    async def create_analogy(
        self,
        concept: str,
        language: str,
        grade_level: str,
        cultural_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create culturally relevant analogies"""
        try:
            if not cultural_context:
                cultural_context = await get_cultural_context(language)
            
            analogy = await create_cultural_analogies(
                concept=concept,
                cultural_context=cultural_context,
                grade_level=grade_level,
                model=self.model,
                config=self.config
            )
            
            if language.lower() != 'english':
                analogy = await translate_content(
                    content=analogy,
                    target_language=language,
                    translate_client=self.translate_client
                )
            
            return {
                'content': analogy,
                'language': language,
                'concept': concept,
                'grade_level': grade_level,
                'cultural_context': cultural_context
            }
        
        except Exception as e:
            raise Exception(f"Error creating analogy: {str(e)}") 