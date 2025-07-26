"""
Assessment & Planning Agent
Handles audio-based assessments and lesson planning
"""
from typing import Dict, Any, Optional, List
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import speech_v1
from google.cloud import translate_v2 as translate
from .tools import (
    process_audio_assessment,
    generate_lesson_plan,
    create_educational_game,
    analyze_reading_level
)

class AssessmentPlannerAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.speech_client = speech_v1.SpeechClient()
        self.translate_client = translate.Client()
        
        self.instruction = """You are an expert in educational assessment and planning, 
        specializing in multi-grade Indian classrooms. Your capabilities include:

        1. Audio-based reading assessments
        2. Weekly lesson planning
        3. Educational game generation
        4. Progress tracking
        5. Multi-grade activity structuring

        Always consider:
        - Limited resources in rural settings
        - Multiple grade levels in one classroom
        - Local language requirements
        - Cultural context
        """
        
        self.config = GenerationConfig(
            temperature=0.4,
            top_p=0.8,
            top_k=40
        )
    
    async def assess_reading(
        self,
        audio_content: bytes,
        language: str,
        grade_level: str,
        text_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform audio-based reading assessment"""
        try:
            # Process audio using Speech-to-Text
            transcript = await self._transcribe_audio(
                audio_content=audio_content,
                language=language
            )
            
            # Analyze reading level and provide feedback
            assessment = await process_audio_assessment(
                transcript=transcript,
                expected_text=text_prompt,
                grade_level=grade_level,
                language=language,
                model=self.model,
                config=self.config
            )
            
            return {
                'transcript': transcript,
                'assessment': assessment,
                'language': language,
                'grade_level': grade_level
            }
        
        except Exception as e:
            raise Exception(f"Error performing reading assessment: {str(e)}")
    
    async def create_lesson_plan(
        self,
        subjects: List[str],
        grade_levels: List[str],
        duration_days: int = 5,
        language: str = 'english'
    ) -> Dict[str, Any]:
        """Generate a weekly lesson plan"""
        try:
            # Generate comprehensive lesson plan
            lesson_plan = await generate_lesson_plan(
                subjects=subjects,
                grade_levels=grade_levels,
                duration_days=duration_days,
                model=self.model,
                config=self.config
            )
            
            # Translate if needed
            if language.lower() != 'english':
                lesson_plan = await self._translate_lesson_plan(
                    lesson_plan=lesson_plan,
                    target_language=language
                )
            
            return {
                'lesson_plan': lesson_plan,
                'subjects': subjects,
                'grade_levels': grade_levels,
                'duration_days': duration_days,
                'language': language
            }
        
        except Exception as e:
            raise Exception(f"Error creating lesson plan: {str(e)}")
    
    async def generate_educational_game(
        self,
        concept: str,
        grade_levels: List[str],
        game_type: str = 'interactive',
        language: str = 'english'
    ) -> Dict[str, Any]:
        """Generate an educational game"""
        try:
            game = await create_educational_game(
                concept=concept,
                grade_levels=grade_levels,
                game_type=game_type,
                model=self.model,
                config=self.config
            )
            
            if language.lower() != 'english':
                game = await self._translate_game_content(
                    game=game,
                    target_language=language
                )
            
            return {
                'game': game,
                'concept': concept,
                'grade_levels': grade_levels,
                'game_type': game_type,
                'language': language
            }
        
        except Exception as e:
            raise Exception(f"Error generating educational game: {str(e)}")
    
    async def _transcribe_audio(
        self,
        audio_content: bytes,
        language: str
    ) -> str:
        """Transcribe audio using Speech-to-Text"""
        try:
            # Configure audio
            audio = speech_v1.RecognitionAudio(content=audio_content)
            config = speech_v1.RecognitionConfig(
                language_code=language,
                enable_automatic_punctuation=True
            )
            
            # Perform transcription
            response = self.speech_client.recognize(
                config=config,
                audio=audio
            )
            
            # Combine all transcriptions
            transcript = ' '.join(
                result.alternatives[0].transcript
                for result in response.results
            )
            
            return transcript
        
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    async def _translate_lesson_plan(
        self,
        lesson_plan: Dict[str, Any],
        target_language: str
    ) -> Dict[str, Any]:
        """Translate lesson plan content"""
        try:
            # Translate each section while preserving structure
            translated_plan = {}
            for key, value in lesson_plan.items():
                if isinstance(value, str):
                    translated_plan[key] = self.translate_client.translate(
                        value,
                        target_language=target_language
                    )['translatedText']
                elif isinstance(value, list):
                    translated_plan[key] = [
                        self.translate_client.translate(
                            item,
                            target_language=target_language
                        )['translatedText']
                        for item in value
                    ]
                elif isinstance(value, dict):
                    translated_plan[key] = await self._translate_lesson_plan(
                        value,
                        target_language
                    )
                else:
                    translated_plan[key] = value
            
            return translated_plan
        
        except Exception as e:
            raise Exception(f"Error translating lesson plan: {str(e)}")
    
    async def _translate_game_content(
        self,
        game: Dict[str, Any],
        target_language: str
    ) -> Dict[str, Any]:
        """Translate game content"""
        # Similar implementation to _translate_lesson_plan
        pass 