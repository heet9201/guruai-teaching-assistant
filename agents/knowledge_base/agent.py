"""
Knowledge Base Agent
Provides simple, accurate explanations for complex concepts in local languages
"""
from typing import Dict, Any, Optional
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import translate_v2 as translate
from .tools import (
    generate_explanation,
    create_simple_analogy,
    translate_explanation,
    get_grade_appropriate_response
)

class KnowledgeBaseAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.translate_client = translate.Client()
        
        self.instruction = """You are an expert educational knowledge base specializing in 
        providing simple, clear explanations for complex concepts. Your explanations should be:

        1. Grade-appropriate and easy to understand
        2. Rich with local, culturally relevant examples
        3. Supported by simple analogies
        4. Scientifically accurate yet accessible

        Focus Areas:
        - Science concepts
        - Mathematical principles
        - Historical events
        - Geographic phenomena
        - Cultural and social topics
        """
        
        self.config = GenerationConfig(
            temperature=0.3,  # Lower temperature for more factual responses
            top_p=0.8,
            top_k=40
        )
    
    async def explain_concept(
        self,
        question: str,
        language: str,
        grade_level: str,
        include_analogy: bool = True
    ) -> Dict[str, Any]:
        """Generate a simple explanation for a complex concept"""
        try:
            # Generate grade-appropriate explanation
            explanation = await generate_explanation(
                question=question,
                grade_level=grade_level,
                model=self.model,
                config=self.config
            )
            
            # Add analogy if requested
            if include_analogy:
                analogy = await create_simple_analogy(
                    concept=question,
                    grade_level=grade_level,
                    model=self.model,
                    config=self.config
                )
                explanation = f"{explanation}\n\nHere's a simple way to think about it:\n{analogy}"
            
            # Translate if needed
            if language.lower() != 'english':
                explanation = await translate_explanation(
                    content=explanation,
                    target_language=language,
                    translate_client=self.translate_client
                )
            
            return {
                'explanation': explanation,
                'language': language,
                'grade_level': grade_level,
                'question': question,
                'includes_analogy': include_analogy
            }
        
        except Exception as e:
            raise Exception(f"Error generating explanation: {str(e)}")
    
    async def get_follow_up_questions(
        self,
        question: str,
        grade_level: str
    ) -> Dict[str, Any]:
        """Generate relevant follow-up questions to deepen understanding"""
        try:
            response = await self.model.generate_content(
                f"""Based on the question "{question}", generate 3 follow-up questions that would 
                help deepen understanding for a grade {grade_level} student. Questions should be 
                progressively more challenging.""",
                generation_config=self.config
            )
            
            return {
                'original_question': question,
                'follow_up_questions': response.text.split('\n'),
                'grade_level': grade_level
            }
        
        except Exception as e:
            raise Exception(f"Error generating follow-up questions: {str(e)}")
    
    async def check_understanding(
        self,
        concept: str,
        explanation: str,
        grade_level: str
    ) -> Dict[str, Any]:
        """Generate simple questions to check understanding"""
        try:
            response = await self.model.generate_content(
                f"""Create 2-3 simple questions to check if a grade {grade_level} student has 
                understood the concept: "{concept}"\n\nBased on the explanation:\n{explanation}""",
                generation_config=self.config
            )
            
            return {
                'concept': concept,
                'check_questions': response.text.split('\n'),
                'grade_level': grade_level
            }
        
        except Exception as e:
            raise Exception(f"Error generating check questions: {str(e)}") 